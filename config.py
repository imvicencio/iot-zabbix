import os

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/sensors/+")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "zabbix_bridge_v1")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)

# Zabbix Configuration
ZABBIX_SERVER = os.getenv("ZABBIX_SERVER", "127.0.0.1")
ZABBIX_PORT = int(os.getenv("ZABBIX_PORT", 10051))
ZABBIX_HOST_NAME = os.getenv("ZABBIX_HOST_NAME", "IoT_Gateway") # The host defined in Zabbix

# Zabbix Security (PSK) - Optional
# Note: Basic Zabbix Sender (Trapper) relies on IP whitelisting. 
# Explicit token auth is for the HTTP API, but if using PSK encryption for Trapper:
ZABBIX_PSK_IDENTITY = os.getenv("ZABBIX_PSK_IDENTITY", None)
ZABBIX_PSK_KEY = os.getenv("ZABBIX_PSK_KEY", None)

# Application Config
DEVICES_FILE = "devices.json"
