# wifi_sta.py
"""
WiFi Station mode - connects ESP32 to existing WiFi network.

Imports credentials from config.py for easy configuration.
"""

import network
import time

from config import WIFI_SSID, WIFI_PASSWORD


def connect_wifi(timeout=20):
    """
    Connect to WiFi network.

    Args:
        timeout: Max seconds to wait for connection

    Returns:
        tuple: (success: bool, ip: str or None)
    """
    sta = network.WLAN(network.STA_IF)

    # Reset WiFi state to avoid "Internal State Error"
    sta.active(False)
    time.sleep(0.5)
    sta.active(True)

    if sta.isconnected():
        print("WiFi: Already connected")
        return True, sta.ifconfig()[0]

    print("WiFi: Connecting to '{}'...".format(WIFI_SSID))
    sta.connect(WIFI_SSID, WIFI_PASSWORD)

    start = time.time()
    while not sta.isconnected():
        if time.time() - start > timeout:
            print("WiFi: Connection timeout!")
            return False, None
        time.sleep(0.5)
        print(".", end="")

    ip = sta.ifconfig()[0]
    print("\nWiFi: Connected!")
    print("WiFi: IP address:", ip)

    return True, ip


def disconnect_wifi():
    """Disconnect from WiFi."""
    sta = network.WLAN(network.STA_IF)
    sta.disconnect()
    sta.active(False)
    print("WiFi: Disconnected")


def is_connected():
    """Check if WiFi is connected."""
    sta = network.WLAN(network.STA_IF)
    return sta.isconnected()


def get_ip():
    """Get current IP address or None if not connected."""
    sta = network.WLAN(network.STA_IF)
    if sta.isconnected():
        return sta.ifconfig()[0]
    return None
