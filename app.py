import streamlit as st
import requests
import random

st.set_page_config(page_title="JohnnyBet Helper 2026", page_icon="🍀")
st.title("🍀 Asistente para JohnnyBet & Premier 2026")

api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

if st.button('🔍 BUSCAR VALOR PARA JOHNNYBET'):
    # Usamos el endpoint de fixtures con temporada 2025 para enero 2026
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"league": "39", "season": "2025", "next": "10"} 

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        # --- SECCIÓN DE DIAGNÓSTICO ---
        if "errors" in data and data["errors"]:
            st.error(f"Error de la API: {data['errors']}")
            if "token" in str(data["errors"]).lower():
                st.warning("Tu API Key parece ser inválida o ha expirado.")
            return

        partidos = data.get('response', [])

        if not partidos:
            st.warning("La API conectó pero no devolvió partidos. Intenta cambiar 'next': '10' por 'live': 'all' para probar si hay algo en vivo.")
            st.write("Respuesta completa de la API para analizar:", data) # Esto nos dirá la verdad
        else:
            for f in partidos:
                local = f['teams']['home']['name']
                visita = f['teams']['away']['name']
                fixture_id = f['fixture']['id']
                
                with st.expander(f"⚽ {local} vs {visita}"):
                    prob_local = random.randint(40, 65)
                    txt_johnny = f"MATCH: {local} vs {visita}\nPREDICTION: Home Win (1)\nREASONING: Analyzing Premier League 2025/26..."
                    st.text_area("Copiar:", txt_johnny, height=100, key=f"txt_{fixture_id}")
                    st.button(f"Reportar {local}", key=f"btn_{fixture_id}")

    except Exception as e:
        st.error(f"Error crítico en el código: {e}")
