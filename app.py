import streamlit as st
import pandas as pd
import plotly.graph_objects as bg
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import numpy as np

# Configuración de la página a pantalla completa (modo Wide)
st.set_page_config(
    page_title="Entre Nodos 2026 - Resultados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Refresco automático de la página cada 5 segundos (5000 ms)
st_autorefresh(interval=5000, key="datarefresh")

# CSS Personalizado para ocultar menús de Streamlit y fondo oscuro continuo
st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo azul oscuro elegante */
    .stApp {
        background-color: #031027;
        color: #FFFFFF;
    }
    
    /* Estilo del título principal */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# URL del Google Sheets publicado como CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsjcnJXMu3xZYbKErvIrCUoDPbh3IU-x7h1y6EZo8vmHxCIFia8sc_OCF9NWwzvecxUjMf68nzllyr/pub?gid=746117259&single=true&output=csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# Nombres simplificados para el eje X
CATEGORIAS = [
    "Empleados sin\ncargo gerencial\ndirigen agentes\nde IA",
    "La automatización\nreduce tareas\ndonde jóvenes\naprendían",
    "Juicio,\nrazonamiento y\nsíntesis se\nvuelven",
    "La geopolítica\nentra en\ndecisiones antes\nsolo",
    "Crecer\nprofesionalmente\nya no significa\nsolo",
    "Adaptación al\nclima extremo\nentra al trabajo\ngerencial"
]

# Layout en 2 columnas: Título / Pregunta a la izquierda, Gráfica a la derecha
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.markdown("### **Entre Nodos 2026**")
    st.markdown("<h2 class='main-title'>Hacia 2031, ¿cuánto podrían cambiar las siguientes señales de la Administración en Colombia?</h2>", unsafe_allow_html=True)
    st.caption("Puntuación: 1 = Cambio Mínimo | 10 = Cambio Decisivo")
    st.info(f"📥 **Respuestas registradas:** {len(df)}")

with col_right:
    fig = bg.Figure()

    if not df.empty and len(df.columns) >= 7:
        # Extraer solo las columnas de preguntas
        df_preguntas = df.iloc[:, 1:7]
        
        # Mapeo de datos para la gráfica con pequeña variación (jitter) para evitar solapamiento exacto
        np.random.seed(42)
        
        for i, col in enumerate(df_preguntas.columns):
            valores = pd.to_numeric(df_preguntas[col], errors='coerce').dropna()
            
            if not valores.empty:
                # Agregar jitter horizontal leve para mostrar aglomeración/densidad
                x_vals = np.full(len(valores), i) + np.random.uniform(-0.15, 0.15, size=len(valores))
                y_vals = valores.values
                
                fig.add_trace(bg.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='markers',
                    marker=dict(
                        size=14,
                        color='#CCFF00', # Color neón llamativo
                        opacity=0.6,
                        line=dict(width=1, color='#FFFFFF')
                    ),
                    name=CATEGORIAS[i] if i < len(CATEGORIAS) else f"P{i+1}",
                    showlegend=False
                ))

    # Estilizado visual de la gráfica siguiendo el modelo de referencia
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(3, 16, 39, 0.8)',
        height=650,
        margin=dict(l=40, r=40, t=30, b=80),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(CATEGORIAS))),
            ticktext=CATEGORIAS,
            showgrid=False,
            zeroline=False,
            tickfont=dict(color='#FFFFFF', size=11),
            showline=True,
            linecolor='#FFFFFF',
            linewidth=2
        ),
        yaxis=dict(
            title="Calificación",
            range=[0.5, 10.5],
            dtick=1,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.15)',
            gridwidth=1,
            griddash='dot',
            tickfont=dict(color='#FFFFFF', size=12),
            showline=True,
            linecolor='#FFFFFF',
            linewidth=2,
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            ticktext=['1. Cambio Mínimo', '2', '3', '4', '5', '6', '7', '8', '9', '10. Cambio Decisivo']
        )
    )

    st.plotly_chart(fig, use_container_width=True)
