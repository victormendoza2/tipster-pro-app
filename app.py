import streamlit as st
import requests

# 1. Configuración de la Interfaz
st.set_page_config(page_title="JohnnyBet Helper 2026", page_icon="🍀", layout="wide")
st.title("🍀 Asistente Tipster Pro - Enero 2026")

# 2. Tus Credenciales
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# 3. Función para obtener análisis profundo
def obtener_analisis(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    params = {"fixture": fixture_id}
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        return data['response'][0] if data.get('response') else None
    except:
        return None

# 4. Selector de modo en el Sidebar
modo = st.sidebar.selectbox("Selecciona qué buscar:", ["Partidos Próximos", "Partidos En Vivo (Live)"])
league_id = "39" # Premier League

if st.button('🔍 BUSCAR VALOR'):
    url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Ajuste de parámetros según el modo
    if modo == "Partidos En Vivo (Live)":
        params_fixtures = {"live": "all", "league": league_id}
    else:
        # Buscamos los próximos 15 partidos para asegurar resultados en enero
        params_fixtures = {"league": league_id, "season": "2025", "next": "15"} 

    with st.spinner('Conectando con la API de Football...'):
        try:
            res_f = requests.get(url_fixtures, headers=headers, params=params_fixtures)
            data_f = res_f.json()
            partidos = data_f.get('response', [])

            if not partidos:
                st.warning(f"No se encontraron partidos {modo.lower()}. Prueba con el modo 'En Vivo' o verifica si la liga ya terminó su jornada.")
                # Debug por si la API devuelve errores de suscripción
                if data_f.get("errors"):
                    st.error(f"Error técnico: {data_f['errors']}")
            else:
                st.success(f"Se encontraron {len(partidos)} eventos.")
                for p in partidos:
                    f_id = p['fixture']['id']
                    home = p['teams']['home']['name']
                    away = p['teams']['away']['name']
                    status = p['fixture']['status']['long']
                    
                    with st.expander(f"⚽ {home} vs {away} ({status})"):
                        analisis = obtener_analisis(f_id)
                        
                        if analisis:
                            advice = analisis['predictions']['advice']
                            percent = analisis['predictions']['percent']
                            
                            # Razonamiento mejorado para Blogabet/JohnnyBet
                            razonamiento = (
                                f"MATCH: {home} vs {away}\n"
                                f"DATE: {p['fixture']['date'][:10]}\n"
                                f"PICK: {advice}\n\n"
                                f"ANALYSIS: Analysis for the 2025/26 season indicates a strong pattern for this match. "
                                f"Probability model: Home {percent['home']} - Draw {percent['draw']} - Away {percent['away']}. "
                                f"Current team form and defensive stats suggest that '{advice}' offers the best value for this fixture."
                            )
                            
                            st.text_area("Texto para copiar:", razonamiento, height=150, key=f"txt_{f_id}")
                        else:
                            st.info("Análisis detallado no disponible para este partido específico.")
                            
        except Exception as e:
            st.error(f"Error de conexión: {e}")

st.markdown("---")
st.caption("Configuración centralizada para 2026. Recuerda gestionar tus ganancias de Grass y Tipster en una misma cuenta.")
