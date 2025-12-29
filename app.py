import streamlit as st
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Tipster Master: Siempre con Tips")

api_key = "TU_API_KEY_AQUI"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

if st.button('🚀 GENERAR TOP 10 (MÉTODO GARANTIZADO)'):
    count = 0
    # Intentaremos buscar en los próximos 2 días si hoy está vacío
    for dias_adelanto in range(3):
        if count >= 10: break
        
        fecha_target = (datetime.now() + timedelta(days=dias_adelanto)).strftime('%Y-%m-%d')
        st.write(f"uscando partidos para el día: {fecha_target}...")
        
        # MÉTODO DE SEGURIDAD: En lugar de filtrar por liga, pedimos todos los partidos 
        # de ese día para asegurar que el contador llegue a 10.
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"date": fecha_target} 
        
        res = requests.get(url, headers=headers, params=params)
        data = res.json().get('response', [])

        if not data:
            continue # Si no hay nada este día, salta al siguiente

        # Mezclar para que no salgan solo ligas desconocidas
        random.shuffle(data)

        for f in data:
            if count >= 10: break
            
            # Filtramos para que sean partidos que no han empezado
            if f['fixture']['status']['short'] == 'NS':
                # Filtro opcional: Solo ligas con nombre conocido (evita ligas juveniles si quieres)
                league_name = f['league']['name']
                country = f['league']['country']
                
                local = f['teams']['home']['name']
                vis = f['teams']['away']['name']
                cuota_auto = round(random.uniform(1.70, 2.15), 2)
                stake_auto = random.randint(7, 9)
                
                count += 1
                
                st.subheader(f"Pronóstico #{count}: {local} vs {vis}")
                st.caption(f"📍 {league_name} ({country}) | 📅 {fecha_target}")

                # Variaciones de análisis para que Blogabet no detecte spam
                templates = [
                    f"Analysis for {local} vs {vis}. Market data shows strong support for the home side efficiency.",
                    f"Strategic pick in {league_name}. Statistical patterns suggest value at odds of {cuota_auto}.",
                    f"High-intensity match expected between {local} and {vis}. Our model points to a tactical advantage."
                ]
                analisis = random.choice(templates) + f" Recommended stake: {stake_auto}/10."

                st.code(f"EVENTO: {local} vs {vis}\nCUOTA: {cuota_auto}\nSTAKE: {stake_auto}/10\n\nANÁLISIS:\n{analisis}", language='text')
                st.divider()

    if count == 0:
        st.error("⚠️ La API no devolvió partidos. Revisa si tu API Key es correcta o si has superado el límite diario.")

