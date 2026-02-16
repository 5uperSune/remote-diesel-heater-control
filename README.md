# Remote Diesel Heater Control (ESP32)

Goal: Build an ESP32-based gateway that can control and (if possible) read status from a diesel heater controller, and expose a safe remote interface (Wi-Fi initially).

## Project status
- Platform: ESP32 (MicroPython)
- Current focus: Connectivity PoC + UART/protocol groundwork

## Repository structure
- `ENGINEERING_LOG.md` — engineering log (decisions, issues, experiments)
- `src/` — MicroPython source code
  - `wifi/` — Wi-Fi connectivity PoC
  - `uart/` — UART tools (sniffing, parsing, loopback)
  - `tests/` — small verification scripts
- `docs/` — diagrams, notes, screenshots

## Hardware
- Board: NodeMCU ESP-32S (ESP32-WROOM-32)

## Safety note
This project interacts with a fuel heater system. All testing is performed cautiously with safe defaults, rate limiting, and a preference for read-only sniffing until the protocol is understood.
