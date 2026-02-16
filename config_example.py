# config_example.py
"""
Configuration template for ESP32 Heater Controller.

SETUP INSTRUCTIONS:
1. Copy this file to 'config.py'
2. Fill in your own credentials below
3. Upload config.py to ESP32

IMPORTANT: Never commit config.py to git - it contains your passwords!
"""

# ============ WiFi Settings ============
# Your home WiFi network credentials
WIFI_SSID = "YourWiFiName"
WIFI_PASSWORD = "YourWiFiPassword"

# ============ MQTT Settings ============
# HiveMQ Cloud credentials (create free account at hivemq.com)
MQTT_BROKER = "your-cluster.hivemq.cloud"
MQTT_PORT = 8883  # TLS encrypted port
MQTT_USER = "your-username"
MQTT_PASSWORD = "your-mqtt-password"

# MQTT Topics - change 'heater1' to a unique ID for your device
MQTT_TOPIC_PREFIX = "heater1"
# This creates topics:
#   heater1/command  (receive commands: on, off, status)
#   heater1/status   (publish current status)

# ============ Access Point Settings ============
# Fallback AP when WiFi connection fails
AP_SSID = "ESP32-Heater"
AP_PASSWORD = "heater1234"  # Min 8 characters
