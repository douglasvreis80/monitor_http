from flask import Flask, Response
from prometheus_client import start_http_server, Gauge, generate_latest
import requests
import yaml
import time
from threading import Thread

app = Flask(__name__)

# Dicionário para armazenar o gauge
gauge = Gauge('http_health_check', 'Health check status for various endpoints', ['name'])

# Função para carregar endpoints do arquivo YAML
def load_endpoints():
    with open('endpoints.yml', 'r') as file:
        endpoints_config = yaml.safe_load(file)
    return endpoints_config.get('endpoints', [])

# Função para monitorar os endpoints
def monitor_endpoints():
    while True:
        endpoints = load_endpoints()
        # Atualizar a métrica com base nos endpoints
        for endpoint in endpoints:
            url = endpoint['url']
            name = endpoint['name']
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    gauge.labels(name=name).set(1)
                else:
                    gauge.labels(name=name).set(0)
            except requests.RequestException:
                gauge.labels(name=name).set(0)
        time.sleep(60)  # Intervalo de monitoramento (ajuste conforme necessário)

# Rota para expor as métricas no Prometheus
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# Função principal para iniciar o exporter
if __name__ == '__main__':
    start_http_server(8000)
    # Iniciar a thread que monitorará os endpoints
    thread = Thread(target=monitor_endpoints)
    thread.start()
    # Rodar a aplicação Flask
    app.run(host='0.0.0.0', port=5000)
