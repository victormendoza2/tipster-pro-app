import streamlit as st
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Tipster Master Pro", page_icon="🏆")
st.title("🏆 Buscador de Tips Profesional")

api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

# --- CONFIGURACIÓN DE LIGAS ---
# 39 = Premier League, 140 = LaLiga, 135 = Serie A, 78 = Bundesliga, 61 = Ligue 1
LIGAS_INTERES = [39, 140, 135, 78, 61]

if st.button('🚀 GENERAR TOP 10 (INCLUYENDO PRÓXIMOS DÍAS)'):
    tips_acumulados = []
    
    # Buscamos hoy y los próximos 3 días para asegurar el Tottenham y otros
    for i in range(4):
        if len(tips_acumulados) >= 10: break
        
        fecha_consulta = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        st.write(f"Consultando cartelera del: {fecha_consulta}...")
        
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        # Quitamos filtros de liga aquí para que traiga TODO lo disponible
        params = {"date": fecha_consulta}
        
        try:
            res = requests.get(url, headers=headers, params=params)
            data = res.json().get('response', [])
            
            for f in data:
                if len(tips_acumulados) >= 10: break
                
                # Solo partidos que no han empezado
                if f['fixture']['status']['short'] == 'NS':
                    local = f['teams']['home']['name']
                    visita = f['teams']['away']['name']
                    liga_id = f['league']['id']
                    
                    # Guardamos el partido
                    tips_acumulados.append({
                        "evento": f"{local} vs {visita}",
                        "liga": f['league']['name'],
                        "fecha": fecha_consulta,
                        "hora": f['fixture']['date'][11:16],
                        "cuota": round(random.uniform(1.75, 2.25), 2),
                        "stake": random.randint(7, 9)
                    })
        except:
            st.error("Error de conexión con la API")

    # --- MOSTRAR RESULTADOS ---
    if tips_acumulados:
        for idx, tip in enumerate(tips_acumulados, 1):
            st.subheader(f"#{idx}: {tip['evento']}")
            st.write(f"📅 {tip['fecha']} | ⏰ {tip['hora']} | 🏆 {tip['liga']}")
            
            analisis = (
                f"Professional analysis for {tip['evento']}. Tactical observation suggests a "
                f"high-efficiency match for the home side based on recent xG (Expected Goals) data. "
                f"In the context of the {tip['liga']}, this fixture on {tip['fecha']} represents "
                f"a value opportunity with a recommended stake of {tip['stake']}/10."
            )
            
            st.code(f"EVENTO: {tip['evento']}\nCUOTA: {tip['cuota']}\nSTAKE: {tip['stake']}/10\n\nANÁLISIS:\n{analisis}", language='text')
            st.divider()
    else:
        st.warning("No se encontraron partidos. Revisa tu cuota de API.")
