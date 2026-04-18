# MongoDB Atlas paso a paso para Chispa

Esta app ya está lista para conectarse a MongoDB Atlas. Lo único manual es crear el cluster y copiar la URI.

## 1. Crear cuenta e iniciar proyecto

1. Entra a MongoDB Atlas.
2. Crea un proyecto nuevo, por ejemplo: `Chispa`.
3. Crea un cluster nuevo.

## 2. Crear usuario de base de datos

Crea un usuario para la base con:

- usuario: el que tú elijas
- contraseña: genera una robusta
- privilegio recomendado: lectura y escritura sobre cualquier base del proyecto

## 3. Permitir acceso de red

Para pruebas rápidas, agrega temporalmente tu IP actual.

Si luego la app vivirá en Streamlit Cloud, lo más simple al inicio es permitir acceso amplio mientras pruebas y después restringirlo.

## 4. Sacar la cadena de conexión

1. Abre tu cluster.
2. Pulsa `Connect`.
3. Elige la conexión para aplicación o driver.
4. Copia la URI SRV, que se verá parecida a esta:

```
mongodb+srv://USUARIO:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Chispa
```

5. Reemplaza `USUARIO` y `PASSWORD` por tu usuario y contraseña reales.

## 5. Variables que debes llenar

En `.env`:

```
GEMINI_API_KEY=tu_api_key_real
GEMINI_MODEL=gemini-1.5-pro
MONGODB_URI=mongodb+srv://USUARIO:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Chispa
MONGODB_DB=chispa
MONGODB_COLLECTION=solicitudes
```

En `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "tu_api_key_real"
GEMINI_MODEL = "gemini-1.5-pro"
MONGODB_URI = "mongodb+srv://USUARIO:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Chispa"
MONGODB_DB = "chispa"
MONGODB_COLLECTION = "solicitudes"
```

## 6. Probar la conexión

Ejecuta:

```bash
python scripts/setup_mongodb.py
```

Luego:

```bash
python scripts/test_services.py
```

Si ambos salen bien, tu MongoDB ya quedó listo para Chispa.
