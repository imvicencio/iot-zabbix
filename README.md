# MQTT to Zabbix Bridge

This project listens for MQTT messages and forwards them to a Zabbix server using the Zabbix Sender protocol. It is designed to act as a bridge between IoT devices (publishing to MQTT) and a Zabbix monitoring system.

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- Access to an **MQTT Broker** (e.g., Mosquitto, EMQX).
- Access to a **Zabbix Server**.

## Configuration

The application is configured via environment variables. You can set these in the `docker-compose.yml` file or export them in your shell.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MQTT_BROKER` | IP address or hostname of the MQTT Broker. | `localhost` |
| `MQTT_PORT` | Port of the MQTT Broker. | `1883` |
| `MQTT_TOPIC` | Topic to subscribe to. Supports wildcards. | `iot/sensors/+` |
| `MQTT_USERNAME` | Username for MQTT Broker. | `None` |
| `MQTT_PASSWORD` | Password for MQTT Broker. | `None` |
| `ZABBIX_SERVER` | IP address or hostname of the Zabbix Server. | `127.0.0.1` |
| `ZABBIX_PORT` | Port of the Zabbix Trapper. | `10051` |
| `ZABBIX_HOST_NAME` | Host name as configured in Zabbix. | `IoT_Gateway` |

### Device Mapping (`devices.json`)

The `devices.json` file maps MQTT topics or payload keys to Zabbix item keys. Ensure this file is mounted or present in the working directory.

## Execution Instructions

### Option 1: Using Docker Compose (Recommended)

1.  **Edit `docker-compose.yml`**:
    Update the environment variables to match your infrastructure (MQTT Broker IP, Zabbix Server IP, etc.).

    ```yaml
    environment:
      - MQTT_BROKER=192.168.1.100
      - ZABBIX_SERVER=192.168.1.200
    ```

2.  **Start the Service**:
    Run the following command in the project directory:

    ```bash
    docker-compose up -d --build
    ```

3.  **Check Logs**:
    To ensure the bridge is connected and processing messages:

    ```bash
    docker-compose logs -f
    ```

4.  **Stop the Service**:
    ```bash
    docker-compose down
    ```

### Option 2: Running Locally (Python)

If you prefer to run the script without Docker (e.g., for development):

1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    You can export environment variables before running:

    ```bash
    export MQTT_BROKER=localhost
    export ZABBIX_SERVER=localhost
    python main.py
    ```

## Troubleshooting

- **Connection Refused**: Ensure the Zabbix Server allows connections from the bridge's IP (check Zabbix Trapper settings).
- **No Data in Zabbix**: Verify `ZABBIX_HOST_NAME` matches exactly the host name configured in Zabbix, and that item keys in `devices.json` exist for that host.
