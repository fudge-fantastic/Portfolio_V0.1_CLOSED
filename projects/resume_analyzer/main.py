# projects/resume_analyzer/resume_analyzer.py
import os
import re
import pdfplumber
import docx
from groq import Groq
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()
api_key_llama = os.getenv("GROQ_API_KEY")
if not api_key_llama:
    raise ValueError("GROQ_API_KEY environment variable not set")

def generate_text(input_text: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(input_text)
    return response.text

def get_llama_assistance(prompt: str) -> str:
    client = Groq(api_key=api_key_llama)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": ""},
        ],
        temperature=1.5,
        max_tokens=8192,
        top_p=1,
        stream=True,
        stop=None,
    )
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    return response_text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file.file)
    full_text = [para.text.strip() for para in doc.paragraphs]
    return '\n\n'.join(full_text)

def clean_text(text: str) -> str:
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text
