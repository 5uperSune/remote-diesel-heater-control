# mqtt_client.py
"""
MQTT Client for remote heater control via HiveMQ Cloud.

Handles:
- TLS-encrypted connection to HiveMQ
- Subscribing to command topic
- Publishing status updates
- Reconnection on connection loss
"""

import time
from umqtt.simple import MQTTClient
import ssl

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
    MQTT_TOPIC_PREFIX
)

# Topics
TOPIC_COMMAND = MQTT_TOPIC_PREFIX + "/command"
TOPIC_STATUS = MQTT_TOPIC_PREFIX + "/status"


class HeaterMQTT:
    def __init__(self, heater_service):
        self.heater = heater_service
        self.client = None
        self.connected = False

    def connect(self):
        """Connect to MQTT broker with TLS."""
        try:
            # Create unique client ID
            import machine
            client_id = "esp32_heater_" + str(machine.unique_id().hex())

            # SSL context for TLS connection
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.verify_mode = ssl.CERT_NONE  # For simplicity; production should verify

            self.client = MQTTClient(
                client_id,
                MQTT_BROKER,
                port=MQTT_PORT,
                user=MQTT_USER,
                password=MQTT_PASSWORD,
                ssl=ssl_context
            )

            # Set callback for incoming messages
            self.client.set_callback(self._on_message)

            print("MQTT: Connecting to {}:{}...".format(MQTT_BROKER, MQTT_PORT))
            self.client.connect()
            print("MQTT: Connected!")

            # Subscribe to command topic
            self.client.subscribe(TOPIC_COMMAND)
            print("MQTT: Subscribed to", TOPIC_COMMAND)

            # Publish online status
            self.publish_status()

            self.connected = True
            return True

        except Exception as e:
            print("MQTT: Connection failed -", e)
            self.connected = False
            return False

    def _on_message(self, topic, msg):
        """Handle incoming MQTT messages."""
        topic = topic.decode()
        msg = msg.decode().strip().lower()

        print("MQTT: Received '{}' on '{}'".format(msg, topic))

        if topic == TOPIC_COMMAND:
            if msg == "on":
                self.heater.turn_on()
                self.publish_status()
            elif msg == "off":
                self.heater.turn_off()
                self.publish_status()
            elif msg == "status":
                self.publish_status()
            else:
                print("MQTT: Unknown command:", msg)

    def publish_status(self):
        """Publish current heater status."""
        if self.client and self.connected:
            status = self.heater.status()
            self.client.publish(TOPIC_STATUS, status)
            print("MQTT: Published status:", status)

    def check_messages(self):
        """
        Check for new MQTT messages (non-blocking).
        Call this regularly in main loop.
        """
        if self.client and self.connected:
            try:
                self.client.check_msg()
            except Exception as e:
                print("MQTT: Error checking messages -", e)
                self.connected = False

    def disconnect(self):
        """Disconnect from MQTT broker."""
        if self.client:
            try:
                self.client.publish(TOPIC_STATUS, "offline")
                self.client.disconnect()
            except:
                pass
            self.connected = False
            print("MQTT: Disconnected")

    def reconnect(self):
        """Attempt to reconnect to MQTT broker."""
        print("MQTT: Attempting reconnect...")
        self.disconnect()
        time.sleep(2)
        return self.connect()
