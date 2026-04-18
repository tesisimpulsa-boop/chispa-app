# Publicar Chispa y obtener un link público

## 1. Sube el proyecto a GitHub

Dentro de la carpeta del proyecto:

```bash
git init
git add .
git commit -m "Primera versión de Chispa"
git branch -M main
git remote add origin TU_URL_DE_GITHUB
git push -u origin main
```

## 2. Crear app en Streamlit Community Cloud

1. Entra a Streamlit Community Cloud.
2. Conecta tu cuenta de GitHub.
3. Haz clic en `Create app`.
4. Elige tu repositorio.
5. Usa `app.py` como archivo principal.
6. Elige el subdominio que quieras.
7. Despliega.

## 3. Configurar secretos

En la sección de secrets de tu app, pega:

```toml
GEMINI_API_KEY = "tu_api_key_real"
GEMINI_MODEL = "gemini-1.5-pro"
MONGODB_URI = "mongodb+srv://USUARIO:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Chispa"
MONGODB_DB = "chispa"
MONGODB_COLLECTION = "solicitudes"
```

## 4. Link público

Cuando termine el deploy, tendrás una URL tipo:

```
https://tu-subdominio.streamlit.app
```

Ese será tu link público para compartir.
