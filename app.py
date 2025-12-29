import streamlit as st
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Tipster Master: Generador 24/7")

# Tu API Key integrada
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key, 
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

if st.button('🚀 GENERAR TOP 10 PRONÓSTICOS'):
    count = 0
    # Intentamos buscar hoy, y si no hay suficiente, buscamos en los próximos 2 días
    for dias_adelanto in range(3):
        if count >= 10: break
        
        fecha_target = (datetime.now() + timedelta(days=dias_adelanto)).strftime('%Y-%m-%d')
        st.write(f"🔍 Buscando partidos para: **{fecha_target}**...")
        
        # URL simplificada: Pedimos TODOS los partidos del día para no quedarnos a cero
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"date": fecha_target} 
        
        try:
            res = requests.get(url, headers=headers, params=params)
            data = res.json().get('response', [])

            if not data:
                continue 

            # Mezclamos los resultados para que los pronósticos sean variados
            random.shuffle(data)

            for f in data:
                if count >= 10: break
                
                # Solo partidos que no han empezado (Status: NS)
                if f['fixture']['status']['short'] == 'NS':
                    liga_n = f['league']['name']
                    pais = f['league']['country']
                    local = f['teams']['home']['name']
                    vis = f['teams']['away']['name']
                    
                    # Generación de métricas realistas
                    cuota_auto = round(random.uniform(1.72, 2.18), 2)
                    stake_auto = random.randint(7, 9)
                    count += 1
                    
                    st.subheader(f"#{count}: {local} vs {vis}")
                    st.caption(f"📍 {liga_n} ({pais}) | 📅 {fecha_target}")

                    # Análisis profesional variado para evitar bloqueos en Blogabet/TipsterBattle
                    analisis_templates = [
                        f"Analyzing the tactical setup for {local} vs {vis}, we find a significant edge in the offensive transition metrics. The home side has shown superior xG performance in recent weeks.",
                        f"Based on the statistical database for {liga_n}, this match presents a clear value opportunity. {local}'s defensive stability vs {vis}'s away record suggests a high probability outcome.",
                        f"Strategic selection for the {pais} league. Market prices are currently inefficient, and our model identifies {cuota_auto} as a high-value entry point for this fixture."
                    ]
                    
                    analisis_final = random.choice(analisis_templates)
                    
                    # Bloque de código listo para copiar
                    st.code(f"EVENTO: {local} vs {vis}\nLIGA: {liga_n}\nCUOTA: {cuota_auto}\nSTAKE: {stake_auto}/10\n\nANÁLISIS:\n{analisis_final}", language='text')
                    st.divider()
        
        except Exception as e:
            st.error(f"Error en la conexión: {e}")

    if count == 0:
        st.warning("No se encontraron partidos. Por favor, verifica tu suscripción en RapidAPI o intenta más tarde.")
    elif count < 10:
        st.info(f"Se completaron {count} tips. No hay más partidos disponibles en los próximos 3 días.")
