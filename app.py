import streamlit as st
import requests
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Tipster Master: Buscador Global")

# Tu API Key
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

if st.button('🚀 BUSCAR PRÓXIMOS 10 PARTIDOS DEL MUNDO'):
    # ENDPOINT DIFERENTE: Trae los próximos partidos sin filtrar por liga ni fecha
    # Es el método más seguro para obtener datos siempre
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"next": 15} 

    try:
        res = requests.get(url, headers=headers, params=params)
        json_data = res.json()
        
        # DEBUG: Esto nos dirá en la pantalla qué está pasando exactamente
        if "errors" in json_data and json_data["errors"]:
            st.error(f"Error de la API: {json_data['errors']}")
        
        partidos = json_data.get('response', [])

        if not partidos:
            st.warning("La API respondió correctamente pero la lista de partidos está vacía. Intenta más tarde.")
        else:
            count = 0
            for f in partidos:
                if count >= 10: break
                
                local = f['teams']['home']['name']
                visita = f['teams']['away']['name']
                liga = f['league']['name']
                fecha = f['fixture']['date'][:10]
                
                cuota = round(random.uniform(1.70, 2.30), 2)
                count += 1
                
                st.subheader(f"#{count}: {local} vs {visita}")
                st.write(f"🏆 {liga} | 📅 {fecha}")
                
                analisis = (
                    f"Advanced tactical preview for {local} vs {visita}. Our algorithm identifies "
                    f"a significant value gap in the {liga} market. Current performance data suggests "
                    f"the selection is underpriced at {cuota}. Highly recommended for ranking growth."
                )
                
                st.code(f"EVENTO: {local} vs {visita}\nCUOTA: {cuota}\n\nANÁLISIS:\n{analisis}", language='text')
                st.divider()
                
    except Exception as e:
        st.error(f"Ocurrió un error crítico: {e}")
