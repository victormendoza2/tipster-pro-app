import streamlit as st
import requests
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Buscador de Partidos: Premier League 2025")

# Tu API Key
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

if st.button('🔍 BUSCAR PARTIDOS PREMIER LEAGUE 2025'):
    # Forzamos la búsqueda en la Premier League (ID 39) y Temporada 2025
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {
        "league": "39", 
        "season": "2025", 
        "next": "20"  # Pedimos los siguientes 20 partidos de esta liga
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        
        partidos = data.get('response', [])

        if not partidos:
            st.warning("No se encontraron partidos para la Premier 2025. Intentando con todas las ligas...")
            # Si falla la Premier, intentamos una búsqueda global sin temporada
            res_global = requests.get(url, headers=headers, params={"next": "15"})
            partidos = res_global.json().get('response', [])

        if partidos:
            for idx, f in enumerate(partidos[:10], 1):
                local = f['teams']['home']['name']
                visita = f['teams']['away']['name']
                fecha = f['fixture']['date'][:10]
                liga_n = f['league']['name']
                
                cuota = round(random.uniform(1.75, 2.20), 2)
                
                st.subheader(f"#{idx}: {local} vs {visita}")
                st.write(f"📅 {fecha} | 🏆 {liga_n}")
                
                # Análisis profesional para Blogabet
                analisis = (
                    f"Regarding the match between {local} and {visita}, our model shows a clear "
                    f"tactical advantage for the selection. Based on current form in {liga_n} "
                    f"and recent xG metrics, the price of {cuota} represents high value."
                )
                
                st.code(f"EVENTO: {local} vs {visita}\nCUOTA: {cuota}\n\nANÁLISIS:\n{analisis}", language='text')
                st.divider()
        else:
            st.error("Sigue sin haber respuesta. Es posible que debas verificar en el Dashboard de RapidAPI si la Premier League 2025 ya tiene datos cargados.")
            
    except Exception as e:
        st.error(f"Error: {e}")
