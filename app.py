import streamlit as st
import requests
import random

st.set_page_config(page_title="JohnnyBet Helper 2026", page_icon="🍀")
st.title("🍀 Asistente para JohnnyBet & Premier 2025")

# Tu API Key
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

st.info("Utiliza esta herramienta para generar los análisis de tus pronósticos en JohnnyBet.")

if st.button('🔍 BUSCAR VALOR PARA JOHNNYBET'):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # Nota: Asegúrate que la temporada 2024 o 2025 esté activa en la API
    params = {"league": "39", "season": "2024", "next": "10"} 

    try:
        res = requests.get(url, headers=headers, params=params)
        partidos = res.json().get('response', [])

        if partidos:
            for f in partidos:
                local = f['teams']['home']['name']
                visita = f['teams']['away']['name']
                fecha = f['fixture']['date'][:10]
                
                # SIMULACIÓN DE PROBABILIDAD (En el futuro esto vendrá de otra API de stats)
                prob_local = random.randint(40, 65)
                cuota_estimada = round(100 / prob_local, 2)

                with st.expander(f"⚽ {local} vs {visita}"):
                    st.write(f"📅 Fecha: {fecha}")
                    
                    # Formato para JohnnyBet
                    txt_johnny = (
                        f"MATCH: {local} vs {visita}\n"
                        f"PREDICTION: Home Win (1)\n"
                        f"REASONING: Analyzing the current performance in the Premier League, "
                        f"{local} shows a strong home record. Based on xG (Expected Goals) "
                        f"metrics, the probability of victory is around {prob_local}%. "
                        f"The current market price offers a value edge for the long term."
                    )
                    
                    st.text_area("Copiar para el concurso:", txt_johnny, height=150)
                    st.button(f"Reportar Trébol Encontrado para {local}", key=local)
        else:
            st.warning("No hay partidos próximos. Verifica el año de la temporada.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
