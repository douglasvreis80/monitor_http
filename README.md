# Monitoring Stack with Prometheus, Grafana, and Exporters

This project provides a monitoring stack using Prometheus, Grafana, and various exporters to monitor endpoints and applications dynamically. The stack includes configuration files and volume persistence to ensure data integrity.

---

## Table of Contents
- [Overview](#overview)
- [Services](#services)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Steps to Run](#steps-to-run)
- [Configuration](#configuration)
  - [Blackbox Exporter](#blackbox-exporter)
  - [Python Exporter](#python-exporter)
  - [Prometheus](#prometheus)
  - [Alertmanager](#alertmanager)
  - [Grafana](#grafana)
- [Volumes](#volumes)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
This stack allows for monitoring and alerting by combining the following components:

- **Prometheus**: Collects metrics from exporters and other sources.
- **Grafana**: Visualizes the metrics in dashboards.
- **Blackbox Exporter**: Monitors the status of HTTP endpoints.
- **Python Exporter**: Custom exporter to dynamically monitor endpoints.
- **Alertmanager**: Sends alerts based on Prometheus rules.

---

## Services

### 1. **Blackbox Exporter**
- Image: `prom/blackbox-exporter`
- Purpose: HTTP endpoint health checks.
- Port: `9116`
- Configuration: `blackbox.yml`

### 2. **Python Exporter**
- Custom-built image located at `./python_exporter/`.
- Purpose: Dynamically monitor endpoints defined in `endpoints.yml`.
- Ports: `5001` (API), `8002` (Web interface).

### 3. **Prometheus**
- Image: `prom/prometheus:v3.0.1`
- Port: `9091`
- Configuration: `prometheus.yml`
- Persisted data: `prometheus_data` volume.

### 4. **Alertmanager**
- Image: `prom/alertmanager`
- Port: `9094`
- Configuration: `alertmanager.yml`
- Persisted data: `alertmanager_data` volume.

### 5. **Grafana**
- Image: `grafana/grafana-oss:11.4.0`
- Port: `3001`
- Configuration: Datasources and dashboards provisioned from `./etc/grafana/`.
- Persisted data: `grafana_data` volume.

### 6. **Alert Messenger**
- **Image**: `douglasvreis80/alert-messenger:1.1`
- **Purpose**: Receives alerts and forwards them via WhatsApp.
- **Port**: `8001`
- **Configuration**: 
  - **Environment Variables**:
    - `GROUP_ID`: The WhatsApp group ID to send messages.
  - **Working Directory**: `/wwebjs-bot`
- **Command**: `npm start`
- **Restart Policy**: `unless-stopped`

---

## Setup

### Prerequisites
- Docker
- Docker Compose

### Steps to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/douglasvreis80/monitor_http.git
   cd monitor_http
   ```

2. Build the Python Exporter:
   ```bash
   docker-compose build python_exporter
   ```

3. Start the stack:
   ```bash
   docker-compose up -d
   ```

4. Access the services:
   - **Grafana**: [http://localhost:3001](http://localhost:3001)
   - **Prometheus**: [http://localhost:9091](http://localhost:9091)
   - **Blackbox Exporter**: [http://localhost:9116](http://localhost:9116)
   - **Python Exporter**: [http://localhost:5001](http://localhost:5001)
   - **Alertmanager**: [http://localhost:9094](http://localhost:9094)
---
### Connecting the Device to Alert Messenger

1. Ensure the stack is running:
   ```bash
   docker-compose up -d
   ```

2. Open the logs for the alert-messenger container to view the QR Code:
    ```bash
   docker logs -f alert-messenger
    ```

3.  Scan the QR Code using the WhatsApp Web feature on your mobile device:
   1. Open WhatsApp on your phone.
   2. Go to Settings > Linked Devices > Link a Device.
   3. Scan the QR Code displayed in the logs.

Once connected, the container will be able to send WhatsApp messages automatically.

## Configuration

### Blackbox Exporter
- Configuration file: `./blackbox.yml`
- Example HTTP probe configuration:
  ```yaml
  modules:
    http:
      prober: http
      timeout: 5s
      http:
        method: GET
  ```

### Python Exporter
- Configuration file: `./python_exporter/endpoints.yml`
- Example endpoint:
  ```yaml
  - name: example
    url: https://example.com
    interval: 30
  ```

### Prometheus
- Configuration file: `./etc/prometheus/prometheus.yml`
- Example scrape job:
  ```yaml
  scrape_configs:
    - job_name: 'blackbox'
      static_configs:
        - targets:
            - http://blackbox-exporter:9115/probe
  ```

### Alertmanager
- Configuration file: `./etc/alertmanager/alertmanager.yml`
- Example receiver:
  ```yaml
  receivers:
    - name: 'email-alert'
      email_configs:
        - to: 'your-email@example.com'
  ```

### Grafana
- Dashboards are located in `./etc/dashboards/`.
- Datasource configuration is in `./etc/grafana/provisioning/datasources/`.

---

## Volumes
- **prometheus_data**: Stores Prometheus metrics data.
- **alertmanager_data**: Stores Alertmanager data.
- **grafana_data**: Stores Grafana dashboards and settings.

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---
