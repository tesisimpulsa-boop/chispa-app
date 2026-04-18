import os

import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")

if not gemini_key:
    raise SystemExit("Falta GEMINI_API_KEY en tu .env")
if not mongo_uri:
    raise SystemExit("Falta MONGODB_URI en tu .env")

genai.configure(api_key=gemini_key)
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-pro"))
response = model.generate_content("Di exactamente: Conexión Gemini OK")
print("Gemini respondió:", getattr(response, "text", "[sin texto]"))

client = MongoClient(mongo_uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=8000)
print("Mongo ping:", client.admin.command("ping"))
