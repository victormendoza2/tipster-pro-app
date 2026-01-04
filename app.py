import streamlit as st
import requests

# 1. Configuración de la Interfaz
st.set_page_config(page_title="JohnnyBet Pro Helper 2026", page_icon="🍀", layout="wide")
st.title("🍀 Generador de Pronósticos (4 de Enero 2026)")

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

# 4. Lógica de búsqueda por proximidad (Sin errores de fecha)
st.info("Buscando los partidos más próximos en las ligas principales para asegurar coincidencia con JohnnyBet.")

if st.button('🔍 CARGAR PARTIDOS DISPONIBLES'):
    url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Usamos 'next=20' para que traiga los próximos 20 partidos del mundo
    # Esto evita el error de "fecha no encontrada" y trae lo de hoy y mañana.
    params_fixtures = {"next": "20"} 

    with st.spinner('Sincronizando con los servidores de la API...'):
        try:
            res_f = requests.get(url_fixtures, headers=headers, params=params_fixtures)
            data_f = res_f.json()
            partidos = data_f.get('response', [])

            if not partidos:
                st.error("La API no devolvió datos. Revisa si tu suscripción en RapidAPI ha llegado al límite diario.")
                st.json(data_f) # Muestra el error técnico real si existe
            else:
                st.success(f"✅ Se han detectado {len(partidos)} partidos para hoy y mañana.")
                
                for p in partidos:
                    f_id = p['fixture']['id']
                    home = p['teams']['home']['name']
                    away = p['teams']['away']['name']
                    liga = p['league']['name']
                    hora = p['fixture']['date'] # Fecha y hora del partido
                    
                    # Limpiamos la hora para que sea legible
                    hora_legible = hora.replace("T", " ").split("+")[0]

                    with st.expander(f"🏟️ {liga} | {home} vs {away} (Inicio: {hora_legible})"):
                        analisis = obtener_analisis(f_id)
                        
                        if analisis:
                            advice = analisis['predictions']['advice']
                            percent = analisis['predictions']['percent']
                            
                            # Texto optimizado para JohnnyBet/Blogabet
                            texto_tipster = (
                                f"MATCH: {home} vs {away}\n"
                                f"LEAGUE: {liga}\n"
                                f"PICK: {advice}\n\n"
                                f"ARGUMENT: Analysis for January 2026. The statistical model shows "
                                f"probabilities: Home {percent['home']}, Draw {percent['draw']}, Away {percent['away']}. "
                                f"Based on current squad rotation and recent form, the pick '{advice}' "
                                f"holds significant value for this fixture."
                            )
                            
                            st.text_area("Copiar para publicar:", texto_tipster, height=150, key=f"t_{f_id}")
                            
                            # Botón de ayuda visual
                            st.write(f"📊 **Confianza:** Local {percent['home']} | Empate {percent['draw']} | Visita {percent['away']}")
                        else:
                            st.warning("Análisis estadístico no disponible para este evento.")

        except Exception as e:
            st.error(f"Error crítico en el script: {e}")

st.divider()
st.caption("Configuración optimizada para centralización de dispositivos (Mobile, Home, Office). 2026.")
