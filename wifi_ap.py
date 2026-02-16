# wifi_ap.py
"""
Wi-Fi Access Point configuration module.

Provides functions to initialize the ESP32 as a Wi-Fi access point
for local configuration and fallback control.

Credentials loaded from config.py for easy configuration.
"""

import network
import time

from config import AP_SSID, AP_PASSWORD


def start_ap():
    """
    Start the ESP32 in Access Point mode.

    Returns the WLAN object for the AP interface.
    """
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=3)

    time.sleep(1)
    ip = ap.ifconfig()[0]
    print("AP: Started '{}'".format(AP_SSID))
    print("AP: IP address:", ip)

    return ap


def stop_ap():
    """Stop the Access Point."""
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    print("AP: Stopped")
