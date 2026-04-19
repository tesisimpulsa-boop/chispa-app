import base64
import os
from datetime import datetime, timezone
from pathlib import Path

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()
st.set_page_config(page_title="Chispa", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "Logo.png"
GIF_SALUDO = ASSETS_DIR / "Chispa saludando gif.gif"
GIF_PENSANDO = ASSETS_DIR / "Chispa pensando gif.gif"
GIF_EXITO = ASSETS_DIR / "Chispa festejando gif.gif"
AUDIO_BIENVENIDA = ASSETS_DIR / "Bienvenido.mp3"
AUDIO_PENSANDO = ASSETS_DIR / "Pensando.mp3"
AUDIO_EXITO = ASSETS_DIR / "Felicidades.mp3"

AREAS_OBJETIVO = [
    "Creatividad",
    "Emociones",
    "Motricidad",
    "Lenguaje",
    "Socialización",
]

SYSTEM_PROMPT_TEMPLATE = """
Actúa como "Chispa", un experto en psicología educativa y desarrollo infantil.
Tu objetivo es diseñar una actividad manual, recreativa y educativa personalizada, estrictamente sin el uso de pantallas.

Datos del usuario:
- Nombre del niño/a: {nombre}
- Edad: {edad} años
- Objetivo a trabajar: {objetivo}
- Tiempo disponible del padre/tutor: {tiempo}

Instrucciones estrictas de formato y tono:
- Utiliza un tono cálido, elegante, profesional y sumamente respetuoso.
- No incluyas introducciones, saludos genéricos ni expliques tu proceso lógico; ve directamente a la entrega del plan.
- Estructura tu respuesta utilizando exactamente los siguientes apartados en negritas:

**TÍTULO DE LA ACTIVIDAD:**
(Un nombre creativo y llamativo)

**MATERIALES NECESARIOS:**
(Únicamente artículos comunes y seguros que se encuentren en cualquier hogar)

**PASO A PASO:**
(Instrucciones claras, prácticas y concisas)

**HITO DE DESARROLLO:**
(Una explicación breve y profesional de la habilidad cognitiva, motriz o emocional específica que se está fortaleciendo con esta actividad)
""".strip()


def get_secret(key: str, default=None):
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)


def get_required_secret(key: str) -> str:
    value = get_secret(key)
    if not value:
        st.error(f"Falta la configuración obligatoria: {key}")
        st.stop()
    return value


@st.cache_resource(show_spinner=False)
def get_gemini_model():
    api_key = get_required_secret("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model_name = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    return genai.GenerativeModel(model_name)


@st.cache_resource(show_spinner=False)
def get_mongo_collection():
    mongo_uri = get_required_secret("MONGODB_URI")
    db_name = get_secret("MONGODB_DB", "chispa")
    collection_name = get_secret("MONGODB_COLLECTION", "solicitudes")

    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=8000,
        server_api=ServerApi("1"),
    )
    client.admin.command("ping")
    collection = client[db_name][collection_name]
    collection.create_index("created_at")
    collection.create_index([("nombre_nino", 1), ("created_at", -1)])
    return collection


def inject_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&display=swap');

            @keyframes titleFadeGlow {
                0% {
                    opacity: 0;
                    transform: translateY(18px) scale(0.98);
                    filter: blur(4px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                    filter: blur(0);
                }
            }

            .stApp {
                background: radial-gradient(circle at top, #121212 0%, #000000 55%);
                color: #FFFFFF;
            }

            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1100px;
            }

            h1 {
                font-family: 'Baloo 2', cursive !important;
                font-size: 3.4rem !important;
                font-weight: 800 !important;
                line-height: 1.08 !important;
                letter-spacing: 0.02em !important;
                background: linear-gradient(90deg, #ffd54f 0%, #ffb300 45%, #ff8f00 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow:
                    0 0 10px rgba(255, 196, 0, 0.35),
                    0 0 22px rgba(255, 166, 0, 0.28),
                    0 0 40px rgba(255, 140, 0, 0.18);
                animation: titleFadeGlow 1s ease-out both;
                margin-bottom: 0.6rem !important;
            }

            h2, h3 {
                color: #FFCC33;
                letter-spacing: 0.02em;
            }

            p, label, div, span {
                color: #FFFFFF;
            }

            .hero-card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 204, 51, 0.18);
                border-radius: 24px;
                padding: 1.4rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
            }

            .stButton > button,
            .stFormSubmitButton > button {
                background: linear-gradient(90deg, #ffd54f 0%, #ffb300 100%);
                color: #111111 !important;
                border: none;
                border-radius: 14px;
                font-weight: 700;
                font-size: 1.1rem;
                padding: 0.8rem 1.2rem;
            }

            .stTextInput label,
            .stNumberInput label,
            .stSelectbox label {
                color: #FFFFFF !important;
                font-size: 1.45rem !important;
                font-weight: 700 !important;
                opacity: 1 !important;
            }

            .stTextInput input,
            .stNumberInput input {
                background-color: #151515 !important;
                color: #FFFFFF !important;
                border-radius: 12px !important;
                font-size: 1.25rem !important;
                padding: 0.85rem 1rem !important;
            }

            .stSelectbox div[data-baseweb="select"] > div {
                background-color: #151515 !important;
                color: #FFFFFF !important;
                border-radius: 12px !important;
                font-size: 1.25rem !important;
                min-height: 58px !important;
                border: 1px solid #3a3a3a !important;
            }

            .stSelectbox div[data-baseweb="select"] span {
                color: #FFFFFF !important;
            }

            .stSelectbox div[data-baseweb="select"] input {
                color: #FFFFFF !important;
            }

            div[data-baseweb="popover"] {
                background: #151515 !important;
                color: #FFFFFF !important;
                border: 1px solid #333333 !important;
            }

            div[data-baseweb="popover"] * {
                color: #FFFFFF !important;
            }

            div[data-baseweb="menu"] {
                background: #151515 !important;
                color: #FFFFFF !important;
            }

            div[data-baseweb="menu"] * {
                background-color: #151515 !important;
                color: #FFFFFF !important;
            }

            ul[role="listbox"] {
                background-color: #151515 !important;
                color: #FFFFFF !important;
            }

            ul[role="listbox"] li {
                background-color: #151515 !important;
                color: #FFFFFF !important;
                font-size: 1.15rem !important;
            }

            li[role="option"] {
                background-color: #151515 !important;
                color: #FFFFFF !important;
                font-size: 1.15rem !important;
            }

            li[role="option"] * {
                color: #FFFFFF !important;
                background-color: transparent !important;
            }

            li[role="option"]:hover,
            li[role="option"][aria-selected="true"] {
                background-color: #2a2a2a !important;
                color: #FFD54F !important;
            }

            li[role="option"]:hover *,
            li[role="option"][aria-selected="true"] * {
                color: #FFD54F !important;
            }

            div[role="listbox"] {
                background-color: #151515 !important;
                color: #FFFFFF !important;
            }

            div[role="option"] {
                background-color: #151515 !important;
                color: #FFFFFF !important;
                font-size: 1.15rem !important;
            }

            div[role="option"] * {
                color: #FFFFFF !important;
                background-color: transparent !important;
            }

            div[role="option"]:hover,
            div[role="option"][aria-selected="true"] {
                background-color: #2a2a2a !important;
                color: #FFD54F !important;
            }

            div[role="option"]:hover *,
            div[role="option"][aria-selected="true"] * {
                color: #FFD54F !important;
            }

            input::placeholder,
            textarea::placeholder {
                color: #FFFFFF !important;
                opacity: 0.75 !important;
                font-size: 1.1rem !important;
            }

            .caption-box {
                background: rgba(255, 204, 51, 0.08);
                border-left: 4px solid #ffcc33;
                border-radius: 12px;
                padding: 0.95rem 1.1rem;
                margin-top: 0.8rem;
                margin-bottom: 1.2rem;
                color: #FFFFFF !important;
                font-size: 1.08rem;
            }

            .stInfo, .stSuccess, .stError, .stWarning {
                font-size: 1.05rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_image(path: Path, width: int | None = None):
    if path.exists():
        st.image(str(path), width=width)


def show_gif(path: Path, width: int = 520):
    if path.exists():
        st.image(str(path), width=width)


def play_audio_once(key: str, file_path: Path):
    if not file_path.exists():
        return

    played = st.session_state.setdefault("played_audio", set())
    if key in played:
        return

    audio_bytes = file_path.read_bytes()
    b64 = base64.b64encode(audio_bytes).decode()
    mime = "audio/mpeg"
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:{mime};base64,{b64}" type="{mime}">
        </audio>
        """,
        unsafe_allow_html=True,
    )
    played.add(key)


def init_state():
    defaults = {
        "step": "welcome",
        "child_data": None,
        "generated_plan": None,
        "db_saved": False,
        "last_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_prompt(child_data: dict) -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(
        nombre=child_data["nombre"],
        edad=child_data["edad"],
        objetivo=child_data["objetivo"],
        tiempo=child_data["tiempo"],
    )


def generate_plan(child_data: dict) -> str:
    model = get_gemini_model()
    prompt = build_prompt(child_data)
    response = model.generate_content(prompt)
    text = getattr(response, "text", "")
    if not text or not text.strip():
        raise ValueError("Gemini no devolvió contenido utilizable.")
    return text.strip()


def save_to_mongodb(child_data: dict, plan: str):
    collection = get_mongo_collection()
    document = {
        "nombre_nino": child_data["nombre"],
        "edad": int(child_data["edad"]),
        "objetivo": child_data["objetivo"],
        "tiempo_disponible": child_data["tiempo"],
        "plan_generado": plan,
        "created_at": datetime.now(timezone.utc),
        "app": "Chispa",
    }
    collection.insert_one(document)


def reset_app():
    keys_to_clear = [
        "step",
        "child_data",
        "generated_plan",
        "db_saved",
        "last_error",
        "played_audio",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    init_state()


def render_header(current_gif: Path):
    col1, col2 = st.columns([1, 1.35])
    with col1:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=300)
    with col2:
        show_gif(current_gif, width=520)
    st.divider()


def render_welcome_screen():
    play_audio_once("welcome", AUDIO_BIENVENIDA)
    render_header(GIF_SALUDO)

    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 0.5rem;">
            <h1>Chispa: actividades personalizadas para pequeñas mentes</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='caption-box'>Responde estas preguntas y Chispa generará una actividad pedagógica personalizada, sin pantallas y pensada para el momento.</div>",
        unsafe_allow_html=True,
    )

    with st.form("chispa_form"):
        nombre = st.text_input("¿Cómo se llama tu hijo o hija?")
        edad = st.number_input("¿Qué edad tiene?", min_value=0, max_value=12, step=1)
        objetivo = st.selectbox("¿Qué objetivo deseas trabajar hoy?", AREAS_OBJETIVO)
        tiempo = st.text_input("¿Cuánto tiempo disponible tienes hoy?", placeholder="Ej. 20 minutos, 1 hora, toda la tarde")
        submitted = st.form_submit_button("Generar plan pedagógico")

    if submitted:
        errores = []
        if not nombre or not nombre.strip():
            errores.append("Escribe el nombre del niño o niña.")
        if not tiempo or not tiempo.strip():
            errores.append("Escribe el tiempo disponible.")

        if errores:
            for error in errores:
                st.error(error)
            return

        st.session_state.child_data = {
            "nombre": nombre.strip(),
            "edad": int(edad),
            "objetivo": objetivo,
            "tiempo": tiempo.strip(),
        }
        st.session_state.step = "thinking"
        st.rerun()


def render_thinking_screen():
    play_audio_once("thinking", AUDIO_PENSANDO)
    render_header(GIF_PENSANDO)

    st.title("Chispa está diseñando una actividad especial...")
    st.info("Estamos conectando con Gemini para crear una propuesta personalizada.")

    if not st.session_state.child_data:
        st.session_state.step = "welcome"
        st.rerun()

    try:
        with st.spinner("Pensando el mejor plan para este momento..."):
            plan = generate_plan(st.session_state.child_data)
            save_to_mongodb(st.session_state.child_data, plan)

        st.session_state.generated_plan = plan
        st.session_state.db_saved = True
        st.session_state.last_error = None
        st.session_state.step = "result"
        st.rerun()
    except Exception as exc:
        st.session_state.last_error = str(exc)
        st.error(f"Hubo un problema al generar o guardar el plan: {exc}")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Reintentar"):
                st.rerun()
        with col_b:
            if st.button("Volver al inicio"):
                reset_app()
                st.rerun()


def render_result_screen():
    play_audio_once("result", AUDIO_EXITO)
    render_header(GIF_EXITO)

    child = st.session_state.child_data or {}
    plan = st.session_state.generated_plan or ""

    st.title(f"Plan personalizado para {child.get('nombre', 'tu peque')} 🌟")
    st.markdown(
        f"<div class='caption-box'><strong>Edad:</strong> {child.get('edad', '')} años &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Objetivo:</strong> {child.get('objetivo', '')} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Tiempo disponible:</strong> {child.get('tiempo', '')}</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.db_saved:
        st.success("La solicitud y el plan fueron guardados correctamente en la base de datos.")

    st.markdown(plan)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Crear otro plan"):
            reset_app()
            st.rerun()
    with col_b:
        st.download_button(
            "Descargar plan en TXT",
            data=plan.encode("utf-8"),
            file_name=f"plan_chispa_{child.get('nombre', 'nino').replace(' ', '_').lower()}.txt",
            mime="text/plain",
            use_container_width=True,
        )


def main():
    inject_css()
    init_state()

    step = st.session_state.step
    if step == "welcome":
        render_welcome_screen()
    elif step == "thinking":
        render_thinking_screen()
    elif step == "result":
        render_result_screen()
    else:
        reset_app()
        render_welcome_screen()


if __name__ == "__main__":
    main()