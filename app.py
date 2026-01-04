import streamlit as st
import requests
from datetime import datetime

# 1. Configuración de la Interfaz
st.set_page_config(page_title="Tipster Pro 2026", page_icon="🍀", layout="wide")
st.title("🍀 Asistente JohnnyBet - Enero 2026")

# 2. Tus Credenciales
api_key = "490b43bb98msh9ddd6e9a90a13b7p1593f7jsncd3e6635c42d"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# 3. Función para obtener análisis profundo
def obtener_analisis(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    params = {"fixture": fixture_id}
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        return data['response'][0] if data.get('response') else None
    except:
        return None

# 4. Lógica de búsqueda mejorada
if st.button('🔍 BUSCAR PARTIDOS PARA HOY (4 ENE 2026)'):
    # Intentamos primero buscar por la fecha exacta de hoy
    url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    fecha_hoy = "2026-01-04" 
    
    with st.spinner(f'Buscando eventos para {fecha_hoy}...'):
        try:
            # Quitamos el filtro de liga para que aparezca CUALQUIER partido disponible
            res_f = requests.get(url_fixtures, headers=headers, params={"date": fecha_hoy})
            data_f = res_f.json()
            partidos = data_f.get('response', [])

            # Si por la fecha no hay nada, forzamos los siguientes 10 del mundo
            if not partidos:
                st.info("No hay partidos registrados para la fecha exacta, buscando los próximos 10 disponibles...")
                res_f = requests.get(url_fixtures, headers=headers, params={"next": "10"})
                partidos = res_f.json().get('response', [])

            if not partidos:
                st.error("Sigue sin haber respuesta. Esto puede ser un problema de tu suscripción en RapidAPI.")
                if "errors" in data_f: st.write(data_f["errors"])
            else:
                st.success(f"Se encontraron {len(partidos)} partidos.")
                for p in partidos:
                    f_id = p['fixture']['id']
                    home = p['teams']['home']['name']
                    away = p['teams']['away']['name']
                    liga = p['league']['name']
                    
                    with st.expander(f"⚽ {liga}: {home} vs {away}"):
                        analisis = obtener_analisis(f_id)
                        if analisis:
                            advice = analisis['predictions']['advice']
                            percent = analisis['predictions']['percent']
                            
                            texto_tipster = (
                                f"MATCH: {home} vs {away}\n"
                                f"PICK: {advice}\n"
                                f"ANALYSIS: For this match on Jan 4, 2026, the model shows "
                                f"probabilities of Home: {percent['home']}, Draw: {percent['draw']}, Away: {percent['away']}. "
                                f"Strategic value found in {advice}."
                            )
                            st.text_area("Copia esto:", texto_tipster, height=130, key=f"t_{f_id}")
                        else:
                            st.write("Predicción detallada no disponible para este partido.")

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Recuerda centralizar tus pagos de Grass y Tipster. Fecha actual del sistema: 4 de enero de 2026.")
