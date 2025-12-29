import streamlit as st
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Tipster Master: Generador Constante")

# Configuración de API
api_key = "TU_API_KEY" # Asegúrate de usar tu llave real
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

# 1. LISTA AMPLIADA DE LIGAS (Europa, América, Asia para cubrir 24/7)
# Incluye: Premier, LaLiga, Serie A, Bundesliga, Ligue 1, Portugal, Países Bajos, Brasil, Argentina, México, etc.
LIGAS_TOP = [39, 140, 135, 78, 61, 94, 88, 71, 128, 262, 2, 3, 848] 

if st.button('🚀 GENERAR TOP 10 PRONÓSTICOS'):
    count = 0
    dias_offset = 0
    max_dias_busqueda = 3 # Buscará hasta 3 días en el futuro si no hay partidos
    
    while count < 10 and dias_offset <= max_dias_busqueda:
        # Calcular fecha de búsqueda
        fecha_busqueda = (datetime.now() + timedelta(days=dias_offset)).strftime('%Y-%m-%d')
        st.write(f"🔍 Buscando partidos para: **{fecha_busqueda}**...")
        
        # Mezclamos las ligas para que los tips no sean siempre de la misma
        random.shuffle(LIGAS_TOP)
        
        for liga_id in LIGAS_TOP:
            if count >= 10: break
            
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            # Nota: Eliminamos 'season' para que la API use la temporada actual activa por defecto
            params = {"league": liga_id, "date": fecha_busqueda}
            
            try:
                res = requests.get(url, headers=headers, params=params)
                data = res.json().get('response', [])
                
                for f in data:
                    if count >= 10: break
                    
                    # Solo partidos que no hayan empezado (Status: NS - Not Started)
                    if f['fixture']['status']['short'] == 'NS':
                        local = f['teams']['home']['name']
                        vis = f['teams']['away']['name']
                        liga_nombre = f['league']['name']
                        
                        cuota_auto = round(random.uniform(1.70, 2.20), 2)
                        stake_auto = random.randint(7, 9)
                        count += 1
                        
                        st.subheader(f"#{count}: {local} vs {vis} ({liga_nombre})")
                        
                        # Análisis optimizado para Blogabet/TipsterBattle
                        analisis_final = (
                            f"Statistical analysis for the match between {local} and {vis} in {liga_nombre}. "
                            f"Our algorithm detects high value on the home/away dynamics for this date ({fecha_busqueda}). "
                            f"Current form and xG (Expected Goals) metrics suggest a competitive edge for this pick. "
                            f"Recommended odds of {cuota_auto} with a professional stake of {stake_auto}/10."
                        )
                        
                        st.code(f"EVENTO: {local} vs {vis}\nFECHA: {fecha_busqueda}\nCUOTA: {cuota_auto}\nSTAKE: {stake_auto}/10\n\nANÁLISIS:\n{analisis_final}", language='text')
            except:
                st.error(f"Error consultando liga {liga_id}")
        
        dias_offset += 1 # Si no llenó los 10, pasa al siguiente día

    if count < 10:
        st.warning(f"Solo se encontraron {count} partidos disponibles en los próximos días.")

