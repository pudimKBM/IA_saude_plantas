# ESP32-CAM MicroPython Scripts for Plant Quality Monitoring

This directory contains the MicroPython scripts designed to run on an ESP32-CAM for the plant quality monitoring project.

## Files

*   **`c:\Users\anton\Documents\GitHub\IA_saude_plantas\esp32Code\boot.py`**:
    *   This script runs automatically when the ESP32-CAM boots up.
    *   Its primary responsibility is to connect the ESP32-CAM to your Wi-Fi network.
*   **`c:\Users\anton\Documents\GitHub\IA_saude_plantas\esp32Code\main.py`**:
    *   This is the main application script that runs after `boot.py` successfully executes (or attempts to connect to Wi-Fi).
    *   It handles:
        *   Initializing the camera.
        *   Capturing images of the plant at regular intervals.
        *   Deciding whether to process the image locally on the ESP32 or send it to a remote server.
        *   Simulating a lightweight AI model if local processing is chosen.
        *   Sending the image to a remote server for more robust AI processing if remote processing is chosen.
        *   Storing classification results locally on the ESP32's filesystem.

## Prerequisites & Requirements

### Hardware:
*   An ESP32-CAM board (or an ESP32 with a compatible camera module).
*   PSRAM is recommended and used by default in `main.py` for the camera framebuffer (`camera.init(..., fb_location=camera.PSRAM)`).

### Firmware:
*   MicroPython firmware flashed onto the ESP32-CAM.
*   The firmware **must** include the following built-in modules:
    *   `camera`: Essential for all camera operations.
    *   `network`: For Wi-Fi connectivity.
    *   `time`: For delays and timestamping.
    *   `ujson`: For working with JSON data (if interacting with a server that uses JSON).
    *   `os`: For basic operating system interactions, like file logging.
    *   `machine`: For hardware-specific control (e.g., `machine.reset()`).
    *   `urandom`: For generating random numbers (used in the local AI simulation).

### MicroPython Libraries (to be installed on the ESP32's filesystem):
*   **`urequests`**: Required by `main.py` for making HTTP POST requests to the remote server.
    *   Install via the MicroPython REPL:
        *   For MicroPython v1.20+ (using `mip`):
            ```python
            import mip
            mip.install("urequests")
            ```
        *   For older MicroPython versions (using `upip`):
            ```python
            import upip
            upip.install("micropython-urequests")
            ```
        *   Alternatively, manually copy `urequests.py` to the device's `/lib` directory or root.

## Configuration

### 1. `c:\Users\anton\Documents\GitHub\IA_saude_plantas\esp32Code\boot.py`:
*   Modify the following lines with your Wi-Fi credentials:
    ```python
    WIFI_SSID = "SUA_REDE_WIFI"
    WIFI_PASSWORD = "SUA_SENHA_WIFI"
    ```

### 2. `c:\Users\anton\Documents\GitHub\IA_saude_plantas\esp32Code\main.py`:
*   **`PROCESSAMENTO_LOCAL`**:
    *   Set to `True` for the ESP32 to perform (simulated) local AI processing.
    *   Set to `False` to send images to a remote server for processing.
*   If `PROCESSAMENTO_LOCAL = False`, configure the server details:
    ```python
    SERVER_IP = "SEU_IP_DO_SERVIDOR"  # e.g., "192.168.1.100"
    SERVER_PORT = 5000
    ```
*   **`INTERVALO_CAPTURA_SEGUNDOS`**: Adjust the time (in seconds) between image captures.
*   **Camera Initialization (`init_camera()` function)**:
    *   The camera settings (`camera.framesize`, `camera.quality`, etc.) might need adjustment based on your specific ESP32-CAM model and lighting conditions. Consult your camera module's documentation.

## How to Use

1.  **Configure**: Update `boot.py` and `main.py` as described in the "Configuration" section.
2.  **Install Libraries**: Ensure `urequests` is installed on your ESP32-CAM's filesystem.
3.  **Upload Scripts**:
    *   Transfer `c:\Users\anton\Documents\GitHub\IA_saude_plantas\esp32Code\boot.py` to the root directory of your ESP32-CAM's filesystem.
    *   Transfer `c:\Users\anton\Documents\GitHub\IA_saude_plantas\esp32Code\main.py` to the root directory of your ESP32-CAM's filesystem.
    *   Tools like Thonny IDE, `ampy`, or `rshell` can be used for this.
4.  **Run**:
    *   Restart your ESP32-CAM.
    *   `boot.py` will run first, attempting to connect to Wi-Fi.
    *   Then, `main.py` will start, initializing the camera and entering the main loop for image capture and processing.
    *   You can monitor the output via a serial connection to the ESP32 (e.g., using Thonny's REPL, PuTTY, or `screen`).

## Local Data Storage

Results from both local processing and confirmations from remote processing are logged to a file named `resultados_locais.txt` on the ESP32's filesystem.