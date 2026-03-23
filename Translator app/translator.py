import os
import io
import torch
import soundfile as sf
from scipy.signal import resample
from configration import MODEL_NAME
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Remove cached tokens (fix authentication issue)
os.environ.pop("HF_TOKEN", None)
os.environ.pop("HUGGINGFACEHUB_API_TOKEN", None)
os.environ.pop("HUGGINGFACE_TOKEN", None)

device = "cuda" if torch.cuda.is_available() else "cpu"


class TranslatorService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)

        # Speed optimization
        self.model.eval()
        if device == "cuda":
            self.model = self.model.half()

        # Preload English TTS
        self.tts_pipelines = {
            "eng": pipeline(
                "text-to-speech",
                model="facebook/mms-tts-eng",
                device=0 if device == "cuda" else -1
            )
        }

    # Translation
    def translate(self, text, src_lang, tgt_lang):
        self.tokenizer.src_lang = src_lang

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        ).to(device)

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_lang),
                max_new_tokens=120,
                num_beams=1
            )

        translated_text = self.tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )[0]

        return translated_text

    # Slow speech
    def slow_down_audio(self, audio_array, speed=0.75):
        """
        speed < 1.0  → slower speech
        speed = 1.0  → normal
        speed > 1.0  → faster
        """
        new_length = int(len(audio_array) / speed)
        slowed_audio = resample(audio_array, new_length)
        return slowed_audio

    # Text to Speech
    def tts(self, text, lang):
        short_text = text[:120].strip()
        if not short_text:
            short_text = "Translation ready."

        tts_lang = lang.split("_")[0]

        # Load language TTS model if not cached
        if tts_lang not in self.tts_pipelines:
            try:
                self.tts_pipelines[tts_lang] = pipeline(
                    "text-to-speech",
                    model=f"facebook/mms-tts-{tts_lang}",
                    device=0 if device == "cuda" else -1
                )
            except:
                pass

        # Try selected language then fallback English
        for try_lang in [tts_lang, "eng"]:
            if try_lang in self.tts_pipelines:
                try:
                    tts_pipe = self.tts_pipelines[try_lang]
                    audio_output = tts_pipe(short_text)

                    audio_array = audio_output["audio"]

                    if isinstance(audio_array, list):
                        audio_array = audio_array[0]

                    if torch.is_tensor(audio_array):
                        audio_array = audio_array.cpu().numpy()

                    # Slow down speech
                    audio_array = self.slow_down_audio(audio_array, speed=0.75)

                    sample_rate = audio_output.get("sampling_rate", 16000)

                    audio_buffer = io.BytesIO()

                    sf.write(
                        audio_buffer,
                        audio_array,
                        sample_rate,
                        format="WAV",
                        subtype="PCM_16"
                    )

                    audio_bytes = audio_buffer.getvalue()

                    if len(audio_bytes) > 2000:
                        return audio_bytes

                except Exception as e:
                    print("TTS error:", e)
                    continue

        # Fallback silence
        silence = torch.zeros(16000 * 2).numpy()
        audio_buffer = io.BytesIO()

        sf.write(
            audio_buffer,
            silence,
            16000,
            format="WAV",
            subtype="PCM_16"
        )

        return audio_buffer.getvalue()