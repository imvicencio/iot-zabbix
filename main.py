import json
import logging
import sys
import config
from mqtt_listener import MQTTListener

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def load_devices():
    try:
        with open(config.DEVICES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.critical(f"Devices file {config.DEVICES_FILE} not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.critical(f"Invalid JSON in {config.DEVICES_FILE}")
        sys.exit(1)

def main():
    logging.info("Starting EMQX-Zabbix Bridge...")
    
    devices = load_devices()
    logging.info(f"Loaded {len(devices)} devices from configuration.")

    listener = MQTTListener(devices)
    listener.start()

if __name__ == "__main__":
    main()
