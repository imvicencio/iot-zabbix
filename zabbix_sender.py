import logging
from pyzabbix import ZabbixMetric, ZabbixSender
import config

class ZabbixProducer:
    def __init__(self, server=config.ZABBIX_SERVER, port=config.ZABBIX_PORT, host_name=config.ZABBIX_HOST_NAME):
        self.server = server
        self.port = port
        self.host_name = host_name
        self.sender = ZabbixSender(zabbix_server=self.server, zabbix_port=self.port)
        logging.info(f"Initialized ZabbixProducer targeting {self.server}:{self.port} for host {self.host_name}")

    def format_key(self, piso, sala, uuid, metric_name):
        # Key format: temperature.piso7.sala.3.uuid
        # Clean inputs to avoid whitespace issues
        uuid_short = str(uuid).split('-')[-1] # usage request example had x.x.x.x, let's use the last segment for brevity or full if needed.
        # User requested: temperature.piso7.sala.3.x.x.x
        # We'll stick to a clean dot notation.
        
        # metric_name (e.g. temperature)
        return f"{metric_name}.piso{piso}.sala.{sala}.{uuid_short}"

    def send_metrics(self, device_info, data):
        """
        device_info: dict containing 'piso', 'sala', 'uuid'
        data: dict containing metrics like {'temperature': 25.5, 'humidity': 60}
        """
        metrics = []
        piso = device_info.get('piso')
        sala = device_info.get('sala')
        uuid = device_info.get('uuid')

        if not (piso and sala and uuid):
            logging.error("Missing device info for Zabbix key generation.")
            return

        for key, value in data.items():
            if key in ['uuid', 'timestamp']: # Skip non-metric fields
                continue
            
            zabbix_key = self.format_key(piso, sala, uuid, key)
            logging.debug(f"Prepared metric: {zabbix_key} = {value}")
            metrics.append(ZabbixMetric(self.host_name, zabbix_key, value))

        if metrics:
            try:
                logging.info(f"Sending {len(metrics)} metrics to Zabbix...")
                # self.sender.send(metrics) # Uncomment to actually send
                # For safety in dev/demo without a real server, we might want to catch connection errors gently.
                ret = self.sender.send(metrics)
                logging.info(f"Zabbix Send Result: {ret}")
            except Exception as e:
                logging.error(f"Failed to send metrics to Zabbix: {e}")
