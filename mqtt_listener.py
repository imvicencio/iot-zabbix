import json
import logging
import paho.mqtt.client as mqtt
import config
from zabbix_sender import ZabbixProducer

class MQTTListener:
    def __init__(self, devices_map):
        self.client = mqtt.Client(client_id=config.MQTT_CLIENT_ID) 
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.devices = devices_map
        self.zabbix_producer = ZabbixProducer()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to MQTT Broker at {config.MQTT_BROKER}")
            client.subscribe(config.MQTT_TOPIC)
        else:
            logging.error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode()
            logging.debug(f"Received message on {msg.topic}: {payload_str}")
            data = json.loads(payload_str)
            
            uuid = data.get("uuid")
            if not uuid:
                logging.warning("Message received without UUID, ignoring.")
                return

            device_info = self.devices.get(uuid)
            if not device_info:
                logging.warning(f"Device UUID {uuid} not found in configuration.")
                return

            # Enrich data with device info needed for Zabbix Context (though format_key calls this again, passing it clean is good practice)
            # Actually, format_key generates from args.
            # Let's pass the enrich info + data to producer
            
            enrichment = {
                "uuid": uuid,
                "piso": device_info.get("piso"),
                "sala": device_info.get("sala")
            }
            
            self.zabbix_producer.send_metrics(enrichment, data)

        except json.JSONDecodeError:
            logging.error("Failed to decode JSON payload")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def start(self):
        try:
            logging.info(f"Connecting to {config.MQTT_BROKER}:{config.MQTT_PORT}...")
            self.client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            logging.info("Stopping MQTT Listener...")
            self.client.disconnect()
        except Exception as e:
            logging.critical(f"MQTT Connection error: {e}")
