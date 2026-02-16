# Agent Task – Architecture and Quality Review

## Context
This project implements remote control of a diesel heater using an ESP32
running MicroPython. The system currently consists of multiple Python modules
(e.g. main.py, wifi_ap.py, http_server.py) and is under active development.

The goal is to evolve the codebase into a robust, safe, and maintainable
Software Engineering–quality system.

## Primary Goals
The codebase must be:

1. **Safe**
   - No undefined behavior
   - No uncontrolled side effects
   - Clear separation between control logic, networking, and hardware interaction

2. **User-friendly**
   - Clear structure and naming
   - Easy to understand for a new developer
   - Predictable behavior from a user perspective

3. **Modular**
   - Each responsibility should live in its own file/module
   - No “god files” that do too much
   - main.py should act as an orchestrator only

4. **Robust**
   - Errors must be caught and handled gracefully
   - No crashes on malformed input or network issues
   - System should fail safely and predictably

## Secondary Goals (Important)
- Designed for **embedded constraints** (ESP32 / MicroPython)
- No unnecessary dependencies
- Clear state handling (explicit state model preferred)
- Easy to extend later (e.g. MQTT, OTA, hardware integration)

## Task Instructions
1. Read all Python files in this directory.
2. Explain the current architecture and responsibilities of each file.
3. Identify weaknesses related to safety, robustness, and modularity.
4. Propose concrete improvements to:
   - file/module structure
   - error handling strategy
   - state management
5. Do **not** modify any files yet.
6. Do **not** install dependencies or run external commands.

## Constraints
- Read-only analysis only
- No file writes
- No network access
- No assumptions about unavailable hardware

## Expected Output
- A clear architectural explanation
- A prioritized list of improvements
- Justification for each proposed change
- Suggestions aligned with good Software Engineering practice
