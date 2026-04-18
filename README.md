# Chispa App

Aplicación en Streamlit para generar actividades pedagógicas personalizadas con Gemini y guardar cada solicitud en MongoDB.

## Incluye

- `app.py`: app principal.
- `assets/`: logo, GIFs y audios.
- `.streamlit/secrets.example.toml`: secrets para local o despliegue.
- `.env.example`: plantilla para correr local.
- `scripts/setup_mongodb.py`: inicializa la colección y prueba la conexión.
- `scripts/test_services.py`: prueba Gemini y MongoDB.
- `docker-compose.mongo-local.yml`: MongoDB local opcional.
- `MONGODB_ATLAS_PASO_A_PASO.md`: guía exacta para crear Atlas.
- `PUBLICAR_EN_STREAMLIT.md`: guía exacta para sacar tu link público.

## Correr localmente

1. Crea un entorno virtual.
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copia `.env.example` a `.env` y pega tus valores reales.
4. Copia `.streamlit/secrets.example.toml` a `.streamlit/secrets.toml` y pega los mismos valores.
5. Inicializa MongoDB:
   ```bash
   python scripts/setup_mongodb.py
   ```
6. Prueba servicios:
   ```bash
   python scripts/test_services.py
   ```
7. Ejecuta la app:
   ```bash
   streamlit run app.py
   ```

## Variables necesarias

- `GEMINI_API_KEY`
- `GEMINI_MODEL` opcional
- `MONGODB_URI`
- `MONGODB_DB`
- `MONGODB_COLLECTION`

## Nota importante

Yo sí pude generarte el código y los archivos de configuración, pero no puedo crear tu cluster real de MongoDB Atlas ni desplegar la app en tu cuenta de Streamlit desde aquí porque eso exige entrar a tus cuentas y usar tus credenciales reales.
