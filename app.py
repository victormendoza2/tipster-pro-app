import streamlit as st
import requests
import random
from datetime import datetime

st.set_page_config(page_title="JohnnyBet Fix", page_icon="🍀")
st.title("🍀 Diagnóstico de Conexión API")

# Tu API Key
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

if st.button('🔍 PROBAR CONEXIÓN AHORA'):
    # Cambiamos 'next' por un rango de fechas para asegurar resultados
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Probamos con la temporada 2025 (Premier League 25/26)
    params = {
        "league": "39", 
        "season": "2025",
        "from": hoy,
        "to": "2026-01-20" # Buscamos partidos de las próximas 2 semanas
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        status = response.status_code
        data = response.json()

        if status != 200:
            st.error(f"Error de Servidor: Código {status}")
            st.write(data) # Aquí verás si tu suscripción expiró
        
        elif data.get("errors"):
            st.error(f"La API devolvió un error: {data['errors']}")
            st.info("💡 Si el error es 'Too many requests' o 'Key not active', revisa tu cuenta en RapidAPI.")

        else:
            partidos = data.get('response', [])
            if not partidos:
                st.warning(f"No hay partidos programados en la Premier del {hoy} al 2026-01-20.")
                st.write("Respuesta completa de la API:", data)
            else:
                st.success(f"¡Se encontraron {len(partidos)} partidos!")
                for f in partidos:
                    local = f['teams']['home']['name']
                    visita = f['teams']['away']['name']
                    with st.expander(f"⚽ {local} vs {visita}"):
                        st.write(f"Fecha: {f['fixture']['date']}")
                        st.code(f"Análisis para JohnnyBet generado.")

    except Exception as e:
        st.error(f"Error de ejecución: {e}")
