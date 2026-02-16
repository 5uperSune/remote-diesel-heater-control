"""
main.py

Application entry point and system orchestrator for the ESP32 heater controller.

Startup sequence:
1. Initialize heater service (with LED indicators)
2. Connect to WiFi (STA mode) for internet access
3. Start AP mode as fallback for local access
4. Connect to MQTT broker for remote control
5. Start HTTP server for local web interface

Dual-mode operation:
- Local control via HTTP (AP or STA network)
- Remote control via MQTT (from anywhere in the world)
"""

import time
from heater_service import HeaterService
from wifi_sta import connect_wifi, is_connected
from wifi_ap import start_ap
from mqtt_client import HeaterMQTT
from http_server import HttpServer


def main():
    print("=" * 40)
    print("ESP32 Heater Controller")
    print("=" * 40)

    # 1. Initialize heater service
    print("\n[1/4] Initializing heater service...")
    try:
        heater = HeaterService()
    except Exception as e:
        print("FATAL: HeaterService init failed -", e)
        return  # Cannot continue without heater

    # 2. Connect to WiFi (STA mode)
    print("\n[2/4] Connecting to WiFi...")
    wifi_ok = False
    ip = None
    try:
        wifi_ok, ip = connect_wifi(timeout=20)
    except Exception as e:
        print("WiFi: Connection error -", e)
        wifi_ok = False

    # 3. Start AP mode as fallback
    print("\n[3/4] Starting AP fallback...")
    try:
        start_ap()
    except Exception as e:
        print("AP: Failed to start -", e)
        # Continue anyway - WiFi might work

    # 4. Connect to MQTT (if WiFi connected)
    mqtt = None
    if wifi_ok:
        print("\n[4/4] Connecting to MQTT broker...")
        try:
            mqtt = HeaterMQTT(heater)
            if not mqtt.connect():
                print("MQTT: Will retry later...")
        except Exception as e:
            print("MQTT: Init error -", e)
            mqtt = None
    else:
        print("\n[4/4] Skipping MQTT (no WiFi)")

    # 5. Start main loop with HTTP server and MQTT
    print("\n" + "=" * 40)
    print("System ready!")
    print("Local HTTP: http://192.168.4.1/")
    if wifi_ok:
        print("WiFi HTTP:  http://{}/".format(ip))
    print("=" * 40 + "\n")

    # Run combined HTTP + MQTT loop
    run_server_loop(heater, mqtt)


def run_server_loop(heater, mqtt):
    """
    Main server loop handling both HTTP and MQTT.

    Uses socket timeout to allow checking MQTT messages
    between HTTP requests.
    """
    import socket

    # Create HTTP server with dependency injection
    http = HttpServer(heater)

    addr = ("0.0.0.0", 80)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(1.0)  # 1 second timeout for non-blocking

    print("HTTP server listening on port 80")

    mqtt_reconnect_timer = 0

    while True:
        # HTTP request handling
        try:
            client, client_addr = s.accept()
            print("HTTP client:", client_addr)
            http.handle_client(client)
        except OSError:
            # Timeout - normal operation, no request received
            pass
        except Exception as e:
            print("HTTP: Unexpected error -", e)
            # Continue loop, don't crash

        # MQTT message handling
        try:
            if mqtt and mqtt.connected:
                mqtt.check_messages()
            elif mqtt and not mqtt.connected:
                # Try to reconnect every 30 seconds
                mqtt_reconnect_timer += 1
                if mqtt_reconnect_timer > 30:
                    mqtt_reconnect_timer = 0
                    mqtt.reconnect()
        except Exception as e:
            print("MQTT: Loop error -", e)
            if mqtt:
                mqtt.connected = False


if __name__ == "__main__":
    main()
