import streamlit as st
import requests

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="JohnnyBet Ultimate Helper 2026", page_icon="🏆", layout="wide")
st.title("🏆 Generador Definitivo de Pronósticos")
st.subheader("Configuración para 04 de Enero, 2026")

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

# --- INTERFAZ DE USUARIO ---
st.sidebar.header("Control de Búsqueda")
opcion = st.sidebar.radio("Método de obtención:", 
                         ["Próximos 15 partidos (Global)", 
                          "Solo Premier League", 
                          "Partidos en Vivo ahora"])

if st.button("🚀 OBTENER PARTIDOS AHORA"):
    partidos = []
    
    with st.spinner("Consultando servidores de API-Football..."):
        if "Próximos" in opcion:
            data = get_data("fixtures", {"next": "15"})
        elif "Premier" in opcion:
            data = get_data("fixtures", {"league": "39", "season": "2025", "next": "10"})
        else:
            data = get_data("fixtures", {"live": "all"})

        # --- VERIFICACIÓN DE ERRORES ---
        if data.get("errors"):
            st.error(f"La API devolvió un error: {data['errors']}")
            st.info("Nota: Verifica si tienes activada la suscripción gratuita o de pago en el dashboard de RapidAPI.")
        else:
            partidos = data.get("response", [])

    if not partidos:
        st.warning("No se encontraron partidos con este filtro. Intenta con 'Próximos 15 partidos (Global)'.")
        st.write("Respuesta completa del servidor (Debug):", data)
    else:
        st.success(f"¡Éxito! Encontrados {len(partidos)} partidos.")
        
        for p in partidos:
            f_id = p['fixture']['id']
            home = p['teams']['home']['name']
            away = p['teams']['away']['name']
            league = p['league']['name']
            
            with st.expander(f"📌 {league}: {home} vs {away}"):
                # Obtener predicción para este fixture
                pred_data = get_data("predictions", {"fixture": f_id})
                
                if pred_data.get("response"):
                    res = pred_data["response"][0]
                    advice = res['predictions']['advice']
                    probs = res['predictions']['percent']
                    
                    # Formato optimizado para copiar y pegar
                    texto_final = (
                        f"MATCH: {home} vs {away}\n"
                        f"PICK: {advice}\n"
                        f"REASONING: Statistical analysis for Jan 2026 shows a win probability of "
                        f"{probs['home']} for home and {probs['away']} for away. "
                        f"Current team momentum supports the '{advice}' selection for JohnnyBet users."
                    )
                    
                    st.text_area("Copiar análisis:", texto_final, height=120, key=f"area_{f_id}")
                    st.write(f"**Confianza:** Casa: {probs['home']} | Empate: {probs['draw']} | Fuera: {probs['away']}")
                else:
                    st.write("No hay predicción detallada, pero puedes usar los datos de la liga para tu estrategia.")

st.markdown("---")
st.caption("Recuerda: Si estás usando Grass en este mismo equipo, este script no interfiere con tu conexión.")
