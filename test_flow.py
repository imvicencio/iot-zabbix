import logging
import json
import unittest
from unittest.mock import MagicMock, patch
from mqtt_listener import MQTTListener

# Mock config to avoid env var issues
import config
config.MQTT_BROKER = "test_broker"
config.ZABBIX_SERVER = "test_zabbix"

class TestBridgeFlow(unittest.TestCase):
    def setUp(self):
        # Sample Device Map
        self.devices = {
            "550e8400-e29b-41d4-a716-446655440000": {
                "piso": 7,
                "sala": 3,
                "name": "test_sensor"
            }
        }
        
    @patch('mqtt_listener.mqtt.Client')
    @patch('zabbix_sender.ZabbixSender')
    def test_flow(self, mock_zabbix_sender_cls, mock_mqtt_client_cls):
        # Setup Mocks
        mock_zabbix_instance = mock_zabbix_sender_cls.return_value
        # We want to verify send is called
        mock_zabbix_instance.send.return_value = "processed: 1; failed: 0; total: 1; seconds spent: 0.000100"

        listener = MQTTListener(self.devices)
        
        # Simulate incoming message
        class MockMessage:
            topic = "iot/sensors/telemetry"
            payload = json.dumps({
                "uuid": "550e8400-e29b-41d4-a716-446655440000",
                "temperature": 25.5,
                "humidity": 45.0,
                "timestamp": 1234567890
            }).encode()

        # Call the on_message handler directly
        listener.on_message(None, None, MockMessage())

        # Assert Zabbix Sender was called
        self.assertTrue(mock_zabbix_instance.send.called)
        
        # Verify the metrics content
        # args[0] is the list of metrics passed to send()
        metrics_sent = mock_zabbix_instance.send.call_args[0][0]
        
        # We expect 2 metrics (temp, humidity), timestamp and uuid are skipped
        self.assertEqual(len(metrics_sent), 2)
        
        # Check keys
        keys = [m.key for m in metrics_sent]
        self.assertIn("temperature.piso7.sala.3.446655440000", keys)
        self.assertIn("humidity.piso7.sala.3.446655440000", keys)
        
        print("\nSUCCESS: Verification test passed! Metrics were correctly formatted and sent to (mock) Zabbix.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL) # Silence app logs for clean test output
    unittest.main()
