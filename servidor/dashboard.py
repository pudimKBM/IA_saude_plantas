# /home/user/esp32_plant_project/dashboard_code/dashboard.py
import streamlit as st
import pandas as pd
import json
import os

# Caminho para o arquivo de resultados e para a pasta de imagens
# Ajuste este caminho se o dashboard estiver em um local diferente em relação ao server_code
SERVER_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'server_code', 'data')
RESULTS_FILE = os.path.join(SERVER_DATA_PATH, 'results.json')
IMAGES_FOLDER = os.path.join(SERVER_DATA_PATH, 'images')

st.set_page_config(page_title="Dashboard Qualidade da Planta", layout="wide")

st.title("🌿 Dashboard de Monitoramento da Qualidade da Planta")

def load_results():
    """Carrega os resultados do arquivo JSON."""
    if not os.path.exists(RESULTS_FILE):
        st.warning(f"Arquivo de resultados não encontrado: {RESULTS_FILE}")
        return pd.DataFrame()
    try:
        with open(RESULTS_FILE, 'r') as f:
            data = json.load(f)
        if not data: # Se o arquivo estiver vazio
            return pd.DataFrame()
        return pd.DataFrame(data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        st.error(f"Erro ao carregar ou decodificar o arquivo de resultados: {e}")
        return pd.DataFrame()

results_df = load_results()

if results_df.empty:
    st.info("Ainda não há resultados para exibir. Certifique-se de que o servidor está rodando e o ESP32 está enviando dados.")
else:
    st.header("Últimos Resultados Registrados")

    # Ordenar por timestamp (mais recente primeiro)
    results_df['timestamp'] = pd.to_datetime(results_df['timestamp'])
    results_df = results_df.sort_values(by='timestamp', ascending=False)

    st.dataframe(results_df[['timestamp', 'classification', 'image_filename', 'processed_by']])

    st.header("Visualizar Imagens e Detalhes")
    if 'image_filename' in results_df.columns:
        selected_image_filename = st.selectbox("Selecione uma imagem para visualizar:", results_df['image_filename'].unique())
        if selected_image_filename:
            image_path = os.path.join(IMAGES_FOLDER, selected_image_filename)
            if os.path.exists(image_path):
                st.image(image_path, caption=f"Imagem: {selected_image_filename}", use_column_width=True)
                details = results_df[results_df['image_filename'] == selected_image_filename].iloc[0]
                st.write(f"**Classificação:** {details['classification']}")
                st.write(f"**Data/Hora:** {details['timestamp']}")
            else:
                st.error(f"Arquivo de imagem não encontrado: {image_path}")

st.sidebar.button("Atualizar Dados") # O Streamlit re-executa o script ao interagir com widgets