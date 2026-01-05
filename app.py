import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="JohnnyBet Ultimate Helper", page_icon="🏆", layout="wide")
st.title("🏆 Generador de Pronósticos Multifecha")

# --- CREDENCIALES ---
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_data(endpoint, params):
    url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- INTERFAZ DE USUARIO (SIDEBAR) ---
st.sidebar.header("Configuración de Filtros")

# Selector de Fecha Dinámico
hoy = datetime.now()
opciones_fecha = {
    "Hoy": hoy.strftime('%Y-%m-%d'),
    "Mañana": (hoy + timedelta(days=1)).strftime('%Y-%m-%d'),
    "Pasado Mañana": (hoy + timedelta(days=2)).strftime('%Y-%m-%d')
}
fecha_seleccionada = st.sidebar.selectbox("Selecciona el día de los partidos:", list(opciones_fecha.keys()))
fecha_query = opciones_fecha[fecha_seleccionada]

opcion = st.sidebar.radio("Ámbito de búsqueda:", 
                         ["Todo el mundo", 
                          "Solo Premier League", 
                          "En Vivo (Solo hoy)"])

# --- LÓGICA PRINCIPAL ---
if st.button(f"🚀 BUSCAR PARTIDOS PARA: {fecha_seleccionada.upper()}"):
    partidos = []
    
    with st.spinner(f"Consultando API para el {fecha_query}..."):
        if "En Vivo" in opcion:
            data = get_data("fixtures", {"live": "all"})
        elif "Premier" in opcion:
            # Temporada 2025 para partidos de Enero 2026
            data = get_data("fixtures", {"league": "39", "season": "2025", "date": fecha_query})
        else:
            data = get_data("fixtures", {"date": fecha_query})

        if data.get("errors"):
            st.error(f"Error de API: {data['errors']}")
        else:
            partidos = data.get("response", [])

    if not partidos:
        st.warning(f"No hay partidos registrados para el {fecha_query} con el filtro seleccionado.")
    else:
        st.success(f"¡Éxito! Encontrados {len(partidos)} partidos.")
        
        for p in partidos:
            f_id = p['fixture']['id']
            home = p['teams']['home']['name']
            away = p['teams']['away']['name']
            league = p['league']['name']
            hora = p['fixture']['date'][11:16] # Extrae HH:MM
            
            with st.expander(f"📌 [{hora}] {league}: {home} vs {away}"):
                pred_data = get_data("predictions", {"fixture": f_id})
                
                if pred_data.get("response"):
                    res = pred_data["response"][0]
                    advice = res['predictions']['advice']
                    probs = res['predictions']['percent']
                    
                    texto_final = (
                        f"MATCH: {home} vs {away}\n"
                        f"DATE: {fecha_query} | LEAGUE: {league}\n"
                        f"PICK: {advice}\n"
                        f"REASONING: Professional analysis for {fecha_query} shows win probabilities: "
                        f"Home: {probs['home']}, Draw: {probs['draw']}, Away: {probs['away']}. "
                        f"Data supports the '{advice}' strategy for JohnnyBet tipsters."
                    )
                    
                    st.text_area("Análisis listo para copiar:", texto_final, height=140, key=f"area_{f_id}")
                    st.write(f"**Confianza:** Casa: {probs['home']} | Empate: {probs['draw']} | Fuera: {probs['away']}")
                else:
                    st.write("Predicción detallada no disponible para este encuentro aún.")

st.markdown("---")
st.caption(f"Actualizado: {hoy.strftime('%d/%m/%Y')}. Compatible con ejecución simultánea de Grass.")
