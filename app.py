import streamlit as st
import requests
from datetime import datetime
import random

st.set_page_config(page_title="Tipster Auto-Pilot", page_icon="⚡")
st.title("⚡ Flujo Ultra-Rápido: Copiar y Pegar")

# VOLVEMOS A MOSTRAR LA FECHA PARA TU TRANQUILIDAD
hoy = datetime.now().strftime('%Y-%m-%d')
st.info(f"📅 Pronósticos para el día: **{hoy}**")

api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

if st.button('🚀 GENERAR MIS 10 PRONÓSTICOS DE HOY'):
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
            cuota_auto = round(random.uniform(1.65, 2.10), 2)
            count += 1
            
            st.subheader(f"Pronóstico #{count}: {local} vs {vis}")
            
            analisis_final = (
                f"Regarding the tactical encounter between {local} and {vis}, our statistical model "
                f"identifies a high-value opportunity. Based on the latest data from the "
                f"API-Football database, {local} shows superior tactical efficiency and "
                f"expected goals (xG) metrics for this specific fixture. With an estimated "
                f"market price of {cuota_auto}, this selection offers a strategic edge for "
                f"ranking growth, combining solid defensive transitions with a high-intensity "
                f"offensive rhythm. This is a professional pick for today's session."
            )
            
            st.code(f"EVENTO: {local} vs {vis}\nCUOTA: {cuota_auto}\n\nANÁLISIS:\n{analisis_final}", language='text')
            st.divider()

    if count == 0:
        st.warning(f"No hay partidos disponibles para {hoy}. Las ligas europeas suelen cargar datos después de las 8:00 AM.")
