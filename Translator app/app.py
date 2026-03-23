import pyperclip
import streamlit as st
from configration import LANGUAGES
from translator import TranslatorService

st.set_page_config(page_title="Translator")

st.title("Translator")

# Session state initialization
if "result" not in st.session_state:
    st.session_state.result = ""

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "target_lang_code" not in st.session_state:
    st.session_state.target_lang_code = ""

@st.cache_resource
def load_translator():
    return TranslatorService()

translator = load_translator()

# Language selection
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source Language", list(LANGUAGES.keys()))

with col2:
    target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()))

# Text input
text = st.text_area("Enter text", height=150)

# Translate
if st.button("Translate"):
    if text.strip():
        with st.spinner("Translating..."):
            result = translator.translate(
                text,
                LANGUAGES[source_lang],
                LANGUAGES[target_lang]
            )

        st.session_state.result = result
        st.session_state.target_lang_code = LANGUAGES[target_lang]

        # Reset audio when new translation happens
        st.session_state.audio_bytes = None

    else:
        st.warning("Enter text first")

# Show result
if st.session_state.result:
    st.subheader("Translated Text")
    st.write(st.session_state.result)

    col_btn1, col_btn2 = st.columns(2)

    # Copy button
    with col_btn1:
        if st.button("Copy to Clipboard"):
            pyperclip.copy(st.session_state.result)
            st.success("Copied to clipboard!")

    # Speak button
    with col_btn2:
        if st.button("Speak"):
            with st.spinner("Generating speech..."):
                st.session_state.audio_bytes = translator.tts(
                    st.session_state.result,
                    st.session_state.target_lang_code
                )

        # Play audio if available
        if st.session_state.audio_bytes:
            st.audio(st.session_state.audio_bytes, format="audio/wav")