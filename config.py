# File: backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_groq_api_key():
    return os.getenv("GROQ_API_KEY")

def get_groq_model():
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")