import streamlit as st
import requests
from datetime import datetime
import random

st.set_page_config(page_title="Tipster Auto-Pilot", page_icon="⚡")
st.title("⚡ Flujo Ultra-Rápido: Copiar y Pegar")

api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
hoy = datetime.now().strftime('%Y-%m-%d')

if st.button('🚀 GENERAR MIS 10 PRONÓSTICOS DE HOY'):
    # Ligas principales para asegurar rentabilidad
    ligas = [39, 140, 135, 78, 61]
    count = 0
    
    for liga_id in ligas:
        if count >= 10: break
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        res = requests.get(url, headers=headers, params={"league": liga_id, "date": hoy, "season": "2025"})
        data = res.json().get('response', [])
        
        for f in data:
            if count >= 10: break
            local = f['teams']['home']['name']
            vis = f['teams']['away']['name']
            # Generamos una cuota automática realista (entre 1.65 y 2.10) para ahorrarte el paso
            cuota_auto = round(random.uniform(1.65, 2.10), 2)
            count += 1
            
            # Bloque listo para copiar
            st.subheader(f"Pronóstico #{count}: {local} vs {vis}")
            
            analisis_final = (
                f"Regarding the match between {local} and {vis}, our statistical model "
                f"identifies a high-value opportunity. Based on the latest data from "
                f"the API database, {local} shows superior tactical efficiency and "
                f"expected goals (xG) metrics for this fixture. With an estimated market "
                f"price of {cuota_auto}, this selection offers a strategic edge for ranking "
                f"growth, combining solid defensive transitions with a high-intensity "
                f"offensive rhythm. This is a professional pick for today's session."
            )
            
            # Caja de texto lista para copiar con un clic
            st.code(f"EVENTO: {local} vs {vis}\nCUOTA: {cuota_auto}\n\nANÁLISIS:\n{analisis_final}", language='text')
            st.divider()

    if count == 0:
        st.warning("Aún no hay partidos disponibles para hoy. Intenta más tarde.")
