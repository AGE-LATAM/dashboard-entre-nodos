import streamlit as st
import pandas as pd
import plotly.graph_objects as bg
import numpy as np

# Configuración de la página a pantalla completa
st.set_page_config(
    page_title="Entre Nodos 2026 - Resultados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Refresco automático de la página cada 4 segundos (4000 ms)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=4000, key="datarefresh")
except Exception:
    pass

# CSS Personalizado con Paleta de Marca, Fuente CendrickNode y Layout Oscuro
st.markdown("""
    <style>
    /* Importación de la fuente personalizada si existe en el repositorio */
    @font-face {
        font-family: 'CendrickNode';
        src: url('CendrickNode-Extended.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }

    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem;}

    /* Fondo principal con color exacto de marca #011533 */
    .stApp {
        background-color: #011533;
        color: #FFFFFF;
        font-family: 'CendrickNode', 'Helvetica Neue', sans-serif;
    }

    /* Títulos e información */
    .brand-title {
        font-family: 'CendrickNode', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    
    .subtitle-info {
        color: #00E6FF;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .badge-count {
        background-color: rgba(0, 230, 255, 0.15);
        border: 1px solid #00E6FF;
        color: #FFFFFF;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 14px;
        display: inline-block;
        margin-top: 10px;
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
    except Exception:
        return pd.DataFrame()

df = load_data()

# Textos de las 6 preguntas para el eje X (exactamente como la gráfica de referencia)
CATEGORIAS_PREGUNTAS = [
    "Empleados sin<br>cargo gerencial<br>dirigen agentes<br>de IA Quién dirige",
    "La automatización<br>reduce tareas<br>donde jóvenes<br>aprendían<br>trabajando Cómo<br>se aprende",
    "Juicio,<br>razonamiento y<br>síntesis se<br>vuelven<br>diferenciales<br>educativos Qué<br>vale saber",
    "La geopolítica<br>entra en<br>decisiones antes<br>solo empresariales<br>Dónde se decide",
    "Crecer<br>profesionalmente<br>ya no significa solo<br>ascender Cómo<br>progresa la<br>carrera",
    "Adaptación al<br>clima extremo<br>entra al trabajo<br>gerencial Qué<br>nuevos problemas<br>gestiona"
]

# Paleta de colores rotativa para los puntos según la marca
PALETA_PUNTOS = ['#BFF400', '#00E6FF', '#FFFFFF', '#BFF400', '#00E6FF', '#FFFFFF']

# Estructura principal en 2 columnas: Menú e Información a la izquierda, Gráfica gigante a la derecha
col_info, col_chart = st.columns([1, 2.6])

with col_info:
    # Intento de cargar el logo si existe en el repo
    try:
        st.image("logo.png", width=180)
    except Exception:
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
                    # Jitter leve horizontal para simular el mapa de calor por densidad de puntos
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

    # Diseño gráfico estilizado en concordancia exacta con la imagen de referencia del cliente
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#011533',
        height=680,
        margin=dict(l=50, r=30, t=20, b=120),
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
            range=[-0.5, 5.5] # Forzar visualización exacta de las 6 columnas
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
