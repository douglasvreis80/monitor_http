import yaml
from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Gauge
import requests
import time
import threading

app = Flask(__name__)

# Variável global para armazenar os endpoints
endpoints = []

# Métrica Prometheus
endpoint_status = Gauge('endpoint_up', 'Status of HTTP endpoint', ['name', 'url'])

# Função para carregar endpoints do arquivo YAML
def load_endpoints():
    global endpoints
    try:
        with open('endpoints.yml', 'r') as file:
            config = yaml.safe_load(file)
            endpoints = config.get('endpoints', [])
    except FileNotFoundError:
        print("Arquivo endpoints.yml não encontrado.")
        endpoints = []

# Função para salvar endpoints no arquivo YAML
def save_endpoints():
    with open('endpoints.yml', 'w') as file:
        yaml.dump({'endpoints': endpoints}, file)

# Função para checar o status dos endpoints
def check_endpoint_status():
    while True:
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint['url'], timeout=5)
                if response.status_code == 200:
                    endpoint_status.labels(endpoint['name'], endpoint['url']).set(1)
                else:
                    endpoint_status.labels(endpoint['name'], endpoint['url']).set(0)
            except requests.exceptions.RequestException:
                endpoint_status.labels(endpoint['name'], endpoint['url']).set(0)
        time.sleep(30)  # Checa a cada 30 segundos

# Rota para listar todos os endpoints
@app.route('/endpoints', methods=['GET'])
def get_endpoints():
    return jsonify(endpoints), 200

# Rota para adicionar um novo endpoint
@app.route('/endpoints', methods=['POST'])
def add_endpoint():
    new_endpoint = request.json
    # Verifica se o endpoint já existe
    if any(e['name'] == new_endpoint['name'] for e in endpoints):
        return jsonify({"status": "error", "message": "Endpoint já existe."}), 400
    endpoints.append(new_endpoint)
    save_endpoints()  # Salva o novo endpoint no arquivo
    return jsonify({"status": "success"}), 201

# Rota para remover um endpoint por nome
@app.route('/endpoints/<name>', methods=['DELETE'])
def remove_endpoint(name):
    global endpoints
    endpoints = [e for e in endpoints if e['name'] != name]
    save_endpoints()  # Salva as alterações no arquivo
    return jsonify({"status": "success"}), 200

# Rota para recarregar endpoints (carregar novamente do YAML)
@app.route('/reload', methods=['POST'])
def reload_endpoints():
    load_endpoints()  # Recarrega os endpoints do arquivo YAML
    return jsonify({"status": "success"}), 200

# Inicializa o servidor HTTP do Prometheus
if __name__ == '__main__':
    # Carrega os endpoints do arquivo YAML ao iniciar o serviço
    load_endpoints()

    # Inicia o HTTP server para expor as métricas na porta 8000
    start_http_server(8000)

    # Inicia a thread que faz a checagem dos endpoints continuamente
    status_thread = threading.Thread(target=check_endpoint_status)
    status_thread.daemon = True  # Thread daemon que termina junto com o processo principal
    status_thread.start()

    # Inicia o servidor Flask na porta 5000
    app.run(host='0.0.0.0', port=5000)
