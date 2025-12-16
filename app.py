import streamlit as st
import fitz  # PyMuPDF
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="📄 PDF Question Answering Bot")
st.title("📄 Ask Questions About Your PDF")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_gpt(question, context):
    prompt = f"""
You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

# Logic
if uploaded_file:
    with st.spinner("Reading PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF loaded and processed.")

    question = st.text_input("Ask a question about the PDF:")
    if question:
        with st.spinner("Thinking..."):
            # Limit context to ~4000 tokens max (safe range ~15k chars for GPT-3.5)
            context = pdf_text[:15000]
            answer = ask_gpt(question, context)
            st.markdown("**🤖 Answer:**")
            st.write(answer)
