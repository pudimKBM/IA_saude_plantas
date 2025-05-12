# /home/user/esp32_plant_project/esp32_code/main.py
import camera
import time
import urequests # Necessário instalar: upip.install('micropython-urequests')
import ujson
import os
import machine

# --- Configurações ---
PROCESSAMENTO_LOCAL = False  # True para processamento local, False para remoto

# Configurações do servidor remoto (se PROCESSAMENTO_LOCAL = False)
SERVER_IP = "SEU_IP_DO_SERVIDOR" # Ex: "192.168.1.100"
SERVER_PORT = 5000
SERVER_UPLOAD_URL = f"http://{SERVER_IP}:{SERVER_PORT}/process_image"

INTERVALO_CAPTURA_SEGUNDOS = 60  # Capturar imagem a cada 60 segundos

LOG_FILE_LOCAL = "resultados_locais.txt"

# --- Funções ---

def init_camera():
    """Inicializa a câmera."""
    try:
        # As configurações exatas podem variar dependendo do seu módulo ESP32-CAM e firmware
        # Consulte a documentação do seu firmware MicroPython para ESP32-CAM
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
        # Configurações comuns:
        camera.framesize(camera.FRAME_HVGA) # Resolução (480x320) - ajuste conforme necessário
        camera.quality(10) # 0-63, menor é maior qualidade
        print("Câmera inicializada.")
    except Exception as e:
        print(f"Erro ao inicializar câmera: {e}")
        # Tentar desinicializar e reinicializar pode ajudar em alguns casos
        try:
            camera.deinit()
        except:
            pass
        # Reiniciar o dispositivo pode ser uma opção drástica se a câmera falhar consistentemente
        # machine.reset()
        raise RuntimeError("Falha na inicialização da câmera")

def capture_image():
    """Captura uma imagem da câmera."""
    print("Capturando imagem...")
    try:
        img_data = camera.capture()
        if img_data:
            print(f"Imagem capturada ({len(img_data)} bytes).")
            return img_data
        else:
            print("Falha ao capturar imagem (dados vazios).")
            return None
    except Exception as e:
        print(f"Erro durante a captura da imagem: {e}")
        return None

def run_lightweight_ai_model(image_data):
    """Simula a execução de um modelo de IA leve localmente."""
    print("Executando modelo de IA leve localmente...")
    # Em um cenário real, aqui você usaria TensorFlow Lite para Microcontroladores
    # Esta é uma simulação muito básica.
    import urandom
    qualidades = ["Excelente", "Boa", "Regular", "Ruim"]
    time.sleep(2) # Simula tempo de processamento
    return urandom.choice(qualidades)

def send_image_to_server(image_data):
    """Envia a imagem para o servidor remoto e obtém a classificação."""
    print(f"Enviando imagem para {SERVER_UPLOAD_URL}...")
    try:
        headers = {'Content-Type': 'image/jpeg'}
        response = urequests.post(SERVER_UPLOAD_URL, data=image_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resultado do servidor: {result}")
            response.close() # Importante fechar a resposta para liberar recursos
            return result.get("classification", "Erro na resposta do servidor")
        else:
            print(f"Erro ao enviar imagem: Código {response.status_code}, Resposta: {response.text}")
            response.close()
            return "Falha na comunicação com o servidor"
    except Exception as e:
        print(f"Exceção ao enviar imagem: {e}")
        return "Exceção na comunicação"

def store_result_locally(timestamp, source, classification):
    """Armazena o resultado da classificação localmente."""
    try:
        with open(LOG_FILE_LOCAL, "a") as f:
            log_entry = f"{timestamp},{source},{classification}\n"
            f.write(log_entry)
        print(f"Resultado armazenado localmente: {log_entry.strip()}")
    except Exception as e:
        print(f"Erro ao armazenar resultado localmente: {e}")

# --- Loop Principal ---
def main_loop():
    init_camera()
    
    while True:
        timestamp_iso = time.localtime() # Formato (ano, mes, dia, hora, min, seg, dia_semana, dia_ano)
        timestamp_str = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(timestamp_iso[0], timestamp_iso[1], timestamp_iso[2], timestamp_iso[3], timestamp_iso[4], timestamp_iso[5])

        image_data = capture_image()
        if not image_data:
            print("Não foi possível capturar a imagem. Tentando novamente em breve.")
            time.sleep(INTERVALO_CAPTURA_SEGUNDOS // 2) # Espera um pouco menos antes de tentar de novo
            continue

        if PROCESSAMENTO_LOCAL:
            print("Processamento local selecionado.")
            classification = run_lightweight_ai_model(image_data)
            store_result_locally(timestamp_str, "local_esp32", classification)
        else:
            print("Processamento remoto selecionado.")
            classification = send_image_to_server(image_data)
            store_result_locally(timestamp_str, "remote_server_confirm", classification) # O servidor também armazena

        print(f"Classificação da planta: {classification}")
        print(f"Aguardando {INTERVALO_CAPTURA_SEGUNDOS} segundos para a próxima captura...")
        time.sleep(INTERVALO_CAPTURA_SEGUNDOS)

if __name__ == "__main__":
    main_loop()