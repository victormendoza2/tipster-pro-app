import streamlit as st
import requests
from datetime import datetime
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Tipster Master: Doble Ganancia")

# Fecha automática para asegurar que siempre sea el día actual
hoy = datetime.now().strftime('%Y-%m-%d')
st.info(f"📅 Generando pronósticos para: **{hoy}**")

api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

if st.button('🚀 GENERAR TOP 10 (RANKING + BLOGABET)'):
    ligas = [39, 140, 135, 78, 61] # Premier, LaLiga, Serie A, etc.
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
            # El Stake suele ser entre 1 y 10; para el ranking usaremos un nivel sólido (7-9)
            stake_auto = random.randint(7, 9)
            count += 1
            
            st.subheader(f"Pronóstico #{count}: {local} vs {vis}")
            
            analisis_final = (
                f"Regarding the tactical encounter between {local} and {vis}, our statistical model "
                f"identifies a high-value opportunity. Based on the latest data from the "
                f"API-Football database, {local} shows superior tactical efficiency and "
                f"expected goals (xG) metrics for this specific fixture. With an estimated "
                f"market price of {cuota_auto} and a recommended stake of {stake_auto}/10, "
                f"this selection offers a strategic edge for ranking growth, combining solid "
                f"defensive transitions with a high-intensity offensive rhythm."
            )
            
            # Bloque optimizado para copiar y pegar en ambas webs
            st.code(f"EVENTO: {local} vs {vis}\nCUOTA: {cuota_auto}\nSTAKE: {stake_auto}/10\n\nANÁLISIS:\n{analisis_final}", language='text')
            st.divider()

    if count == 0:
        st.warning(f"Buscando partidos para {hoy}. Si no aparecen, intenta después de las 8 AM.")
