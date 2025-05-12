# /home/user/esp32_plant_project/esp32_code/boot.py
import network
import time

# Configurações do Wi-Fi
WIFI_SSID = "SUA_REDE_WIFI"
WIFI_PASSWORD = "SUA_SENHA_WIFI"

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Conectando ao Wi-Fi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 10  # Segundos de timeout
        start_time = time.time()
        while not sta_if.isconnected() and (time.time() - start_time) < timeout:
            time.sleep(1)
            print(".")
    if sta_if.isconnected():
        print("Conectado ao Wi-Fi!")
        print("Configurações de rede:", sta_if.ifconfig())
    else:
        print("Falha ao conectar ao Wi-Fi.")

connect_wifi()