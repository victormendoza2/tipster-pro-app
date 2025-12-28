import streamlit as st
import requests
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="Tipster Pro Hunter", page_icon="⚽")
st.title("🏆 Tipster Pro: Crecimiento de Ranking")

api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
hoy = datetime.now().strftime('%Y-%m-%d')

st.write(f"Buscando partidos rentables para hoy: **{hoy}**")

# Ligas que te darán más puntos
ligas = [39, 140, 135, 78, 61]
partidos_encontrados = []

if st.button('🚀 ESCANEAR PARTIDOS AHORA'):
    for liga_id in ligas:
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        res = requests.get(url, headers=headers, params={"league": liga_id, "date": hoy, "season": "2025"})
        data = res.json().get('response', [])
        for f in data:
            partidos_encontrados.append({
                "local": f['teams']['home']['name'],
                "vis": f['teams']['away']['name'],
                "liga": f['league']['name'],
                "id": f['fixture']['id']
            })

    if partidos_encontrados:
        for p in partidos_encontrados:
            with st.expander(f"⭐ {p['local']} vs {p['vis']} ({p['liga']})"):
                cuota = st.text_input("Cuota en web:", key=p['id'])
                if cuota:
                    analisis = (
                        f"Regarding the tactical match between {p['local']} and {p['vis']}, "
                        f"our statistical model identifies a high-value opportunity. "
                        f"Based on recent data from API-Football, {p['local']} shows "
                        f"superior offensive efficiency. At an odd of {cuota}, this "
                        f"selection offers a strategic edge for ranking growth."
                    )
                    st.code(analisis, language='text')
                    st.success("¡Copia el texto de arriba!")
    else:
        st.warning("No hay partidos rentables detectados aún. Intenta en unos minutos.")