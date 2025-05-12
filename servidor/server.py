# /home/user/esp32_plant_project/server_code/server.py
from flask import Flask, request, jsonify
import os
import datetime
import random
import time
import json

app = Flask(__name__)

# --- Configurações ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'images')
RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'results.json')
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Cria o diretório se não existir

def run_robust_ai_model(image_path):
    """Simula a execução de um modelo de IA robusto."""
    print(f"Executando modelo de IA robusto para: {image_path}")
    # Em um cenário real, aqui você carregaria a imagem (ex: com Pillow, OpenCV)
    # e usaria um framework de IA (TensorFlow, PyTorch, etc.)
    
    # Simulação:
    time.sleep(random.uniform(0.5, 2.0)) # Simula tempo de processamento
    qualidades = ["Qualidade Superior", "Qualidade Padrão", "Necessita Atenção", "Crítico"]
    return random.choice(qualidades)

def load_results():
    """Carrega os resultados do arquivo JSON."""
    if not os.path.exists(RESULTS_FILE):
        return []
    try:
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return [] # Retorna lista vazia se o JSON estiver malformado

def save_result(result_entry):
    """Salva uma nova entrada de resultado no arquivo JSON."""
    results = load_results()
    results.append(result_entry)
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=4)

@app.route('/process_image', methods=['POST'])
def process_image_route():
    if 'file' not in request.files and not request.data:
        # O ESP32 pode enviar a imagem diretamente no corpo da requisição
        # ou como um arquivo em um formulário multipart.
        # Este exemplo lida com dados brutos no corpo.
        if not request.data:
            return jsonify({"error": "Nenhuma imagem fornecida"}), 400
        image_data = request.data
    elif 'file' in request.files:
         file = request.files['file']
         if file.filename == '':
             return jsonify({"error": "Nenhum arquivo selecionado"}), 400
         image_data = file.read()
    else: # Fallback para request.data se 'file' não estiver presente mas houver dados
        image_data = request.data

    timestamp = datetime.datetime.now()
    filename = f"plant_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        with open(image_path, 'wb') as f:
            f.write(image_data)
        print(f"Imagem salva em: {image_path}")

        # Executa o modelo de IA (simulado)
        classification = run_robust_ai_model(image_path)
        print(f"Classificação: {classification}")

        # Armazena o resultado
        result_entry = {
            "timestamp": timestamp.isoformat(),
            "image_filename": filename, # Apenas o nome do arquivo, não o caminho completo
            "classification": classification,
            "processed_by": "remote_server"
        }
        save_result(result_entry)

        return jsonify({"classification": classification, "image_saved_as": filename}), 200
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Execute com: flask run --host=0.0.0.0 (ou python server.py e ajuste o host/porta abaixo)
    # O host 0.0.0.0 torna o servidor acessível na rede local
    app.run(host='0.0.0.0', port=5000, debug=True)