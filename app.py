import streamlit as st
import pandas as pd
import plotly.graph_objects as bg
import numpy as np
import base64
import os

# Configuración de la página a pantalla completa (modo Wide)
st.set_page_config(
    page_title="Entre Nodos 2026 - Resultados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Refresco automático de la página cada 4 segundos
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=4000, key="datarefresh")
except Exception:
    pass

# Cargar la fuente CendrickNode en Base64 para inyección directa en CSS
font_css = ""
font_file = "CendrickNode-Extended.ttf"
if os.path.exists(font_file):
    with open(font_file, "rb") as f:
        font_data = base64.b64encode(f.read()).decode()
    font_css = f"""
    @font-face {{
        font-family: 'CendrickNode';
        src: url(data:font/ttf;base64,{font_data}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """

# CSS Personalizado con la fuente forzada y la paleta exacta (#011533, #BFF400, #00E6FF)
st.markdown(f"""
    <style>
    {font_css}

    /* Ocultar menús y márgenes predeterminados de Streamlit */
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}

    /* Fondo principal de marca #011533 */
    .stApp {{
        background-color: #011533;
        color: #FFFFFF;
        font-family: 'CendrickNode', sans-serif, 'Helvetica Neue';
    }}

    /* Tipografía aplicada a títulos y textos */
    h1, h2, h3, h4, p, div, span {{
        font-family: 'CendrickNode', sans-serif, 'Helvetica Neue' !important;
    }}

    .brand-title {{
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.25;
        margin-top: 20px;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }}

    .subtitle-info {{
        color: #00E6FF;
        font-size: 14px;
        margin-bottom: 15px;
    }}

    .badge-count {{
        background-color: rgba(0, 230, 255, 0.12);
        border: 1px solid #00E6FF;
        color: #FFFFFF;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 14px;
        display: inline-block;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# URL del Google Sheets publicado como CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsjcnJXMu3xZYbKErvIrCUoDPbh3IU-x7h1y6EZo8vmHxCIFia8sc_OCF9NWwzvecxUjMf68nzllyr/pub?gid=746117259&single=true&output=csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# Textos para las 6 columnas del eje X en el orden exacto del Google Form
CATEGORIAS_PREGUNTAS = [
    "Empleados sin<br>cargo gerencial<br>dirigen agentes<br>de IA Quién dirige",
    "Juicio,<br>razonamiento y<br>síntesis se<br>vuelven<br>diferenciales<br>educativos Qué<br>vale saber",
    "La automatización<br>reduce tareas<br>donde jóvenes<br>aprendían<br>trabajando Cómo<br>se aprende",
    "Adaptación al<br>clima extremo<br>entra al trabajo<br>gerencial Qué<br>nuevos problemas<br>gestiona",
    "La geopolítica<br>entra en<br>decisiones antes<br>solo empresariales<br>Dónde se decide",
    "Crecer<br>profesionalmente<br>ya no significa solo<br>ascender Cómo<br>progresa la<br>carrera"
]

# Colores rotativos de la paleta oficial
PALETA_PUNTOS = ['#BFF400', '#00E6FF', '#FFFFFF', '#BFF400', '#00E6FF', '#FFFFFF']

# Disposición en 2 columnas
col_info, col_chart = st.columns([1, 2.6])

with col_info:
    logo_path = "Logo Entre nodos.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=220)
    else:
        st.markdown("<h2 style='color:#BFF400;'>Entre Nodos</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='brand-title'>Hacia 2031, ¿cuánto podrían cambiar las siguientes señales de la Administración en Colombia?</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-info'>Puntuación: 1 = Cambio Mínimo | 10 = Cambio Decisivo</div>", unsafe_allow_html=True)
    
    total_respuestas = len(df) if not df.empty else 0
    st.markdown(f"<div class='badge-count'>📥 <b>Respuestas registradas:</b> {total_respuestas}</div>", unsafe_allow_html=True)

with col_chart:
    fig = bg.Figure()

    if not df.empty and len(df.columns) >= 7:
        df_preguntas = df.iloc[:, 1:7]
        
        np.random.seed(42)
        
        for i, col in enumerate(df_preguntas.columns):
            if i < len(CATEGORIAS_PREGUNTAS):
                valores = pd.to_numeric(df_preguntas[col], errors='coerce').dropna()
                
                if not valores.empty:
                    # Jitter leve horizontal para simular densidad de puntos
                    x_vals = np.full(len(valores), i) + np.random.uniform(-0.12, 0.12, size=len(valores))
                    y_vals = valores.values
                    
                    color_columna = PALETA_PUNTOS[i % len(PALETA_PUNTOS)]
                    
                    fig.add_trace(bg.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode='markers',
                        marker=dict(
                            size=16,
                            color=color_columna,
                            opacity=0.75,
                            line=dict(width=1, color='#FFFFFF')
                        ),
                        showlegend=False,
                        hoverinfo='y'
                    ))

    # Diseño gráfico con la fuente CendrickNode en los ejes
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#011533',
        height=680,
        margin=dict(l=50, r=30, t=20, b=120),
        font=dict(family='CendrickNode, sans-serif', color='#FFFFFF'),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(6)),
            ticktext=CATEGORIAS_PREGUNTAS,
            showgrid=False,
            zeroline=False,
            tickfont=dict(color='#FFFFFF', size=11, family='CendrickNode, sans-serif'),
            showline=True,
            linecolor='#FFFFFF',
            linewidth=2,
            range=[-0.5, 5.5]
        ),
        yaxis=dict(
            range=[0.5, 10.5],
            dtick=1,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.2)',
            gridwidth=1,
            griddash='dot',
            tickfont=dict(color='#FFFFFF', size=11, family='CendrickNode, sans-serif'),
            showline=True,
            linecolor='#FFFFFF',
            linewidth=2,
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            ticktext=[
                '1. Cambio Mínimo', '2. .....', '3. .....', '4. .....', '5. .....',
                '6. .....', '7. .....', '8. .....', '9. .....', '10. Cambio Decisivo'
            ]
        )
    )

    st.plotly_chart(fig, use_container_width=True)
