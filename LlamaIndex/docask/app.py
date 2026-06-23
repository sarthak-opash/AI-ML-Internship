import os
import tempfile
from pathlib import Path

import streamlit as st

from dotenv import load_dotenv

from llama_parse import LlamaParse

from llama_index.core import (
    Settings,
    VectorStoreIndex,
)
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Streamlit UI
st.set_page_config(
    page_title="LlamaIndex OCR Chatbot"
)

st.title("📄 OCR Chatbot with LlamaIndex")

# Hardcoded Document
uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT)"
)

if not uploaded_file:
    st.info("Upload a document to parse it and ask questions about it.")
    st.stop()

if not os.getenv("GROQ_API_KEY"):
    st.error("Set GROQ_API_KEY in your environment before asking questions.")
    st.stop()


@st.cache_resource(show_spinner=False)
def build_query_engine(file_name: str, file_bytes: bytes):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=Path(file_name).suffix,
    ) as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        parser = LlamaParse(
            result_type="text"
        )

        documents = parser.load_data(
            temp_path
        )

        Settings.llm = Groq(
            model=GROQ_MODEL,
            api_key=os.getenv("GROQ_API_KEY"),
        )
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

        index = VectorStoreIndex.from_documents(
            documents
        )

        return index.as_query_engine()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


with st.spinner("Parsing document and building index..."):
    query_engine = build_query_engine(
        uploaded_file.name,
        uploaded_file.getvalue(),
    )


st.success("Document indexed successfully!")

# Ask Questions
question = st.text_input(
    "Ask a question about the document"
)

if question:

    with st.spinner("Generating answer..."):

        response = query_engine.query(
            question
        )

    st.subheader("Answer")
    
    st.write(response.response)