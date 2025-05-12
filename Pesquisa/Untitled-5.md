# Projeto de Monitoramento de Qualidade de Plantas com ESP32-CAM e IA

Este projeto demonstra um sistema para capturar imagens de plantas usando um ESP32-CAM, processá-las (localmente ou remotamente) usando um modelo de Inteligência Artificial (simulado) para classificar a qualidade da planta, armazenar os resultados e visualizá-los em um dashboard.

## Estrutura do Projeto

```
esp32_plant_project/
├── esp32_code/                 # Código para o ESP32-CAM (MicroPython)
│   ├── boot.py                 # Configuração inicial (ex: Wi-Fi)
│   └── main.py                 # Lógica principal do ESP32
├── server_code/                # Código do servidor (Python/Flask)
│   ├── server.py               # Aplicação Flask para receber imagens e processá-las
│   └── data/                   # Dados gerados pelo servidor
│       ├── images/             # Imagens recebidas do ESP32
│       └── results.json        # Resultados da classificação (formato JSON)
└── dashboard_code/             # Código do dashboard (Python/Streamlit)
    └── dashboard.py            # Aplicação Streamlit para visualização
└── README.md                   # Este arquivo
```

## Configuração e Execução

### 1. ESP32-CAM (`esp32_code/`)

*   **Pré-requisitos**:
    *   ESP32-CAM com firmware MicroPython instalado.
    *   Biblioteca `urequests` instalada no MicroPython (`import mip; mip.install("urequests")` ou `import upip; upip.install('micropython-urequests')`).
*   **Configuração**:
    1.  Edite `/home/user/esp32_plant_project/esp32_code/boot.py`:
        *   Configure `WIFI_SSID` e `WIFI_PASSWORD` com suas credenciais de Wi-Fi.
    2.  Edite `/home/user/esp32_plant_project/esp32_code/main.py`:
        *   Defina `PROCESSAMENTO_LOCAL` como `True` para processamento no ESP32 ou `False` para processamento remoto.
        *   Se `PROCESSAMENTO_LOCAL` for `False`, configure `SERVER_IP` com o endereço IP da máquina que executa o `server.py`. `SERVER_PORT` é 5000 por padrão.
        *   Ajuste `INTERVALO_CAPTURA_SEGUNDOS` conforme necessário.
        *   **Importante**: As funções `init_camera()` e `capture_image()` podem precisar de ajustes específicos para o seu módulo ESP32-CAM e versão do firmware MicroPython. Consulte a documentação do seu firmware.
*   **Execução**:
    *   Transfira `boot.py` e `main.py` para a raiz do sistema de arquivos do ESP32.
    *   Reinicie o ESP32. O `main.py` deve começar a ser executado após a conexão Wi-Fi.

### 2. Servidor (`server_code/`)

*   **Pré-requisitos**: Python 3.x, Flask.
*   **Instalação**:
    ```bash
    pip install Flask
    ```
*   **Execução**:
    1.  Navegue até o diretório `/home/user/esp32_plant_project/server_code/`.
    2.  Execute o servidor:
        ```bash
        python server.py
        ```
        Ou usando o comando `flask`:
        ```bash
        export FLASK_APP=server.py
        flask run --host=0.0.0.0 --port=5000
        ```
    *   O servidor estará escutando em `http://0.0.0.0:5000`. O diretório `data/images/` e o arquivo `data/results.json` serão criados automaticamente.

### 3. Dashboard (`dashboard_code/`)

*   **Pré-requisitos**: Python 3.x, Streamlit, Pandas.
*   **Instalação**:
    ```bash
    pip install streamlit pandas
    ```
*   **Execução**:
    1.  Navegue até o diretório `/home/user/esp32_plant_project/dashboard_code/`.
    2.  Execute o dashboard:
        ```bash
        streamlit run dashboard.py
        ```
    3.  Abra o navegador no endereço fornecido (geralmente `http://localhost:8501`).

## Como Funciona

1.  O **ESP32-CAM** (`main.py`) captura uma imagem da planta em intervalos definidos.
2.  Ele decide se o processamento da imagem ocorrerá **localmente** ou **remotamente** com base na variável `PROCESSAMENTO_LOCAL`.
    *   **Local**: Um modelo de IA leve (simulado em `run_lightweight_ai_model`) é executado no próprio ESP32. O resultado é armazenado em um arquivo de log (`resultados_locais.txt`) no ESP32.
    *   **Remoto**: A imagem é enviada via Wi-Fi para o **Servidor** (`server.py`).
3.  O **Servidor** recebe a imagem, salva-a em `server_code/data/images/`, executa um modelo de IA mais robusto (simulado em `run_robust_ai_model`), e armazena a classificação e metadados em `server_code/data/results.json`. O resultado da classificação também é retornado ao ESP32.
4.  O **ESP32** (no caso de processamento remoto) recebe a classificação do servidor e também pode armazená-la localmente.
5.  O **Dashboard** (`dashboard.py`) lê o arquivo `results.json` do servidor e exibe os dados de classificação, incluindo as imagens capturadas, permitindo ao usuário visualizar o histórico e a qualidade das plantas.

## Próximos Passos e Melhorias

*   **Modelos de IA Reais**: Substituir as funções `run_lightweight_ai_model` e `run_robust_ai_model` por implementações reais de modelos de IA (ex: usando TensorFlow Lite for Microcontrollers no ESP32, e TensorFlow/PyTorch no servidor).
*   **Comunicação Segura**: Implementar HTTPS para o servidor e autenticação.
*   **Banco de Dados**: Usar um banco de dados mais robusto (ex: SQLite, PostgreSQL) no servidor em vez de um arquivo JSON.
*   **Alertas**: Adicionar um sistema de alertas (ex: e-mail, SMS) para classificações críticas.
*   **Interface do Usuário**: Melhorar a interface do dashboard, adicionar filtros, gráficos, etc.
*   **Configuração Dinâmica**: Permitir que o ESP32 obtenha configurações do servidor ou de um arquivo de configuração no cartão SD.
*   **Tratamento de Erros**: Melhorar o tratamento de erros e a resiliência da comunicação.