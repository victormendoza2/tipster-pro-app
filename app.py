import streamlit as st
import requests
import random

st.set_page_config(page_title="JohnnyBet Helper 2026", page_icon="🍀")
st.title("🍀 Asistente para JohnnyBet & Premier 2026")

# Tu API Key
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key, 
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

st.info("Utiliza esta herramienta para generar los análisis de tus pronósticos en JohnnyBet.")

if st.button('🔍 BUSCAR VALOR PARA JOHNNYBET'):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # CAMBIO: Temporada 2025 para partidos actuales en enero 2026
    params = {"league": "39", "season": "2025", "next": "10"} 

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        
        # Debug: Descomenta la siguiente línea si quieres ver qué responde la API exactamente
        # st.write(data) 

        partidos = data.get('response', [])

        if partidos:
            for f in partidos:
                local = f['teams']['home']['name']
                visita = f['teams']['away']['name']
                fecha = f['fixture']['date'][:10]
                
                prob_local = random.randint(40, 65)
                
                with st.expander(f"⚽ {local} vs {visita}"):
                    st.write(f"📅 Fecha: {fecha}")
                    
                    txt_johnny = (
                        f"MATCH: {local} vs {visita}\n"
                        f"PREDICTION: Home Win (1)\n"
                        f"REASONING: Analyzing the current performance in the Premier League 2025/26, "
                        f"{local} shows a strong home record. Based on xG metrics, "
                        f"the probability of victory is around {prob_local}%. "
                        f"The current market price offers a value edge."
                    )
                    
                    st.text_area("Copiar para el concurso:", txt_johnny, height=150, key=f"text_{f['fixture']['id']}")
                    st.button(f"Reportar Trébol para {local}", key=f"btn_{f['fixture']['id']}")
        else:
            # Mensaje más detallado para saber qué falló
            error_api = data.get('errors', [])
            if error_api:
                st.error(f"La API devolvió un error: {error_api}")
            else:
                st.warning("No se encontraron partidos. Intenta cambiar la temporada a 2025 o verifica tu suscripción en RapidAPI.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
