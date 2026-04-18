import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "chispa")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "solicitudes")

if not MONGODB_URI:
    raise SystemExit("Falta MONGODB_URI en tu .env o variables de entorno.")

client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))
client.admin.command("ping")

db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

collection.create_index("created_at")
collection.create_index([("nombre_nino", 1), ("created_at", -1)])

sample_doc = {
    "nombre_nino": "Prueba Chispa",
    "edad": 5,
    "objetivo": "Creatividad",
    "tiempo_disponible": "20 minutos",
    "plan_generado": "Documento de prueba para confirmar la conexión.",
    "created_at": datetime.now(timezone.utc),
    "app": "Chispa-setup",
    "is_setup_test": True,
}

inserted = collection.insert_one(sample_doc)
print("Conexión OK")
print(f"Base: {MONGODB_DB}")
print(f"Colección: {MONGODB_COLLECTION}")
print(f"Documento de prueba insertado: {inserted.inserted_id}")
