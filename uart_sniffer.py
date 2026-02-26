# uart_sniffer.py
"""
UART Sniffer for reverse-engineering heater remote control protocol.

Captures UART data and associates it with user-defined labels.
Designed to be used via HTTP interface for easy protocol analysis.

Hardware setup:
- COM line → 200Ω resistor → PC817 optocoupler input (V1/GND)
- PC817 output (N1) → ESP32 GPIO16 (RX), (ND) → ESP32 GND
- Optocoupler inverts signal, so UART.INV_RX is required
- GPIO17 (TX) must be physically disconnected - NEVER drive COM line!

Protocol: 250 baud, 8N1, half-duplex single-wire COM bus
"""

from machine import UART
import time
import gc

# UART2 pin configuration (RX only - never drive the COM line!)
PIN_RX = 16

# Default settings
DEFAULT_BAUD = 250
CAPTURE_DURATION_MS = 5000  # 5 seconds capture
MAX_CAPTURES = 20  # Prevent memory exhaustion


class UartSniffer:
    def __init__(self, baud=DEFAULT_BAUD, invert_rx=True):
        self.baud = baud
        self.invert_rx = invert_rx
        self.uart = None
        self.captured_commands = []

    def _cleanup_uart(self):
        """Safely cleanup UART."""
        if self.uart:
            try:
                self.uart.deinit()
            except:
                pass
            self.uart = None
        gc.collect()

    def set_baud(self, baud):
        """Change baud rate for next capture."""
        self._cleanup_uart()
        self.baud = baud

    def capture(self, label, duration_ms=CAPTURE_DURATION_MS):
        """
        Capture UART data for a specified duration and label it.
        """
        # Cleanup any previous UART
        self._cleanup_uart()
        time.sleep_ms(100)

        try:
            # tx=17 but GPIO17 must be physically disconnected!
            # tx=-1 is NOT supported on MicroPython v1.27.0
            invert = UART.INV_RX if self.invert_rx else 0
            self.uart = UART(2, baudrate=self.baud, rx=PIN_RX, tx=17, invert=invert)
            self.uart.init(self.baud, bits=8, parity=None, stop=1, rx=PIN_RX, tx=17, invert=invert)
        except Exception as e:
            print("UART init error:", e)
            return {"label": label, "data": b"", "baud": self.baud, "bytes": 0}

        # Clear any pending data
        try:
            if self.uart.any():
                self.uart.read()
        except:
            pass

        print("Capturing '{}' for {}ms at {} baud...".format(
            label, duration_ms, self.baud))

        all_data = bytearray()
        start_time = time.ticks_ms()

        try:
            while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
                if self.uart.any():
                    chunk = self.uart.read()
                    if chunk:
                        all_data.extend(chunk)
                time.sleep_ms(5)
        except Exception as e:
            print("Capture error:", e)
        finally:
            self._cleanup_uart()

        result = {
            "label": label,
            "data": bytes(all_data),
            "baud": self.baud,
            "bytes": len(all_data)
        }

        if len(self.captured_commands) >= MAX_CAPTURES:
            self.captured_commands.pop(0)
            print("Max captures reached, oldest removed")
        self.captured_commands.append(result)
        print("Captured {} bytes for '{}'".format(len(all_data), label))

        gc.collect()
        return result

    def get_all_captures(self):
        return self.captured_commands

    def clear_captures(self):
        self.captured_commands = []
        gc.collect()

    def delete_capture(self, index):
        if 0 <= index < len(self.captured_commands):
            self.captured_commands.pop(index)
            return True
        return False

    def format_hex(self, data):
        return " ".join("{:02X}".format(b) for b in data)

    def format_ascii(self, data):
        result = ""
        for b in data:
            if 32 <= b <= 126:
                result += chr(b)
            else:
                result += "."
        return result


# Global sniffer instance (250 baud, inverted RX for optocoupler)
sniffer = UartSniffer()
