import streamlit as st
import requests

# 1. Configuración de la Interfaz
st.set_page_config(page_title="Tipster Pro AI 2026", page_icon="⚽", layout="wide")

st.title("🚀 Generador Automático de Pronósticos 2026")
st.markdown("---")

# 2. Tus Credenciales (Mantenidas según tu código)
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# 3. Función para obtener el análisis profundo
def obtener_analisis(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    params = {"fixture": fixture_id}
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        if data.get("response"):
            return data["response"][0]
    except:
        return None
    return None

# 4. Botón de Ejecución
if st.button('🔍 BUSCAR PARTIDOS Y GENERAR ARGUMENTOS'):
    # Endpoint de fixtures para la Premier League (ID 39) temporada 2025
    url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params_fixtures = {"league": "39", "season": "2025", "next": "8"} 

    with st.spinner('Extrayendo datos y procesando estrategias...'):
        try:
            res_f = requests.get(url_fixtures, headers=headers, params=params_fixtures)
            data_f = res_f.json()
            partidos = data_f.get('response', [])

            if not partidos:
                st.warning("No hay partidos próximos encontrados.")
            else:
                for p in partidos:
                    f_id = p['fixture']['id']
                    home = p['teams']['home']['name']
                    away = p['teams']['away']['name']
                    
                    # Analizar cada partido
                    analisis = obtener_analisis(f_id)
                    
                    with st.expander(f"📌 {home} vs {away}"):
                        if analisis:
                            # Extraer datos de la predicción
                            advice = analisis['predictions']['advice']
                            percent = analisis['predictions']['percent']
                            comp = analisis['comparison']
                            
                            # Crear el razonamiento automático
                            razonamiento = (
                                f"PREDICTION: {advice}\n\n"
                                f"ANALYSIS: This match in the Premier League 2025/26 shows high statistical value. "
                                f"{home} has an offensive strength of {comp['att']['home']} "
                                f"compared to {away}'s defensive rating of {comp['def']['away']}. "
                                f"The probability model shows a {percent['home']} chance for Home and "
                                f"{percent['away']} for Away. Based on recent H2H, {advice} is the most solid pick."
                            )
                            
                            st.write(f"**Recomendación de la IA:** {advice}")
                            st.text_area("Copia esto en JohnnyBet / Blogabet:", razonamiento, height=180, key=f"text_{f_id}")
                            
                            # Indicadores visuales
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Prob. Local", percent['home'])
                            col2.metric("Prob. Empate", percent['draw'])
                            col3.metric("Prob. Visita", percent['away'])
                        else:
                            st.error("No se pudo generar el análisis detallado.")
                            
        except Exception as e:
            st.error(f"Error crítico: {e}")

# Pie de página informativo
st.markdown("---")
st.info("💡 Tip: Usa este generador para llenar tus perfiles de Tipster automáticamente y centralizar tus ingresos.")
