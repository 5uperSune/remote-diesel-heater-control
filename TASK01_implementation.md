# TASK01: Implementation Plan - Fase 1: Stabilitet

**Dato:** 2026-02-03
**Status:** Godkendt til implementation
**Fase:** 1 af 3
**Fokus:** Fejlhåndtering og robusthed

---

## Oversigt

| # | Ændring | Fil | Risiko |
|---|---------|-----|--------|
| 1.1 | Robust HTTP request parsing | http_server.py | Lav |
| 1.2 | Safe decode med fallback | http_server.py | Lav |
| 1.3 | Exception handling i main loop | main.py | Lav |
| 1.4 | Graceful WiFi/MQTT fejl | main.py | Lav |

---

## 1.1 Robust HTTP Request Parsing

### Nuværende kode (http_server.py linje 34-48)

```python
def handle_client(client):
    try:
        request = client.recv(1024).decode()
        if not request:
            return

        request_line = request.split("\r\n")[0]
        method, path, _ = request_line.split()  # ❌ CRASHER ved malformed!

        # Extract query string if present
        query = ""
        if "?" in path:
            path, query = path.split("?", 1)

        print("HTTP:", method, path)
```

### Ny kode

```python
def handle_client(client):
    try:
        # 1. Modtag data
        raw_request = client.recv(1024)
        if not raw_request:
            return

        # 2. Decode med fejlhåndtering
        try:
            request = raw_request.decode('utf-8')
        except UnicodeDecodeError:
            print("HTTP: Invalid UTF-8 encoding")
            send_response(client, 400, "Bad Request", "Invalid encoding")
            return

        # 3. Parse request line sikkert
        lines = request.split("\r\n")
        if not lines or not lines[0]:
            print("HTTP: Empty request")
            send_response(client, 400, "Bad Request", "Empty request")
            return

        parts = lines[0].split()
        if len(parts) < 2:
            print("HTTP: Malformed request line")
            send_response(client, 400, "Bad Request", "Malformed request")
            return

        method = parts[0]
        path = parts[1]

        # 4. Extract query string
        query = ""
        if "?" in path:
            path, query = path.split("?", 1)

        print("HTTP:", method, path)

        # ... routing fortsætter som før
```

### Hvorfor?

| Problem | Løsning |
|---------|---------|
| `decode()` kan kaste `UnicodeDecodeError` | Try/except med 400 response |
| `split()` kan returnere for få elementer | Check `len(parts) >= 2` |
| Tom request crasher | Early return med check |

---

## 1.2 Exception Wrapper omkring Routing

### Tilføj til handle_client (efter routing)

```python
def handle_client(client):
    try:
        # ... parsing kode fra 1.1 ...

        # Routing med exception handling
        try:
            if path == "/":
                index(client)
            elif path == "/status":
                status(client)
            # ... resten af routing ...
            else:
                not_found(client)
        except Exception as e:
            print("HTTP: Handler error -", e)
            try:
                send_response(client, 500, "Internal Server Error", "Server error")
            except:
                pass  # Client måske allerede disconnected

    except Exception as e:
        print("HTTP: Request error -", e)

    finally:
        try:
            client.close()
        except:
            pass
```

### Hvorfor?

- Uventet fejl i en handler crasher ikke hele serveren
- Client får en 500-fejl i stedet for timeout
- `finally` sikrer socket altid lukkes

---

## 1.3 Robust Main Loop

### Nuværende kode (main.py linje 89-107)

```python
while True:
    try:
        client, client_addr = s.accept()
        print("HTTP client:", client_addr)
        http_server.handle_client(client)
    except OSError:
        pass  # ❌ Fanger kun OSError, andre exceptions crasher

    if mqtt and mqtt.connected:
        mqtt.check_messages()
    elif mqtt and not mqtt.connected:
        mqtt_reconnect_timer += 1
        if mqtt_reconnect_timer > 30:
            mqtt_reconnect_timer = 0
            mqtt.reconnect()
```

### Ny kode

```python
while True:
    # HTTP request handling
    try:
        client, client_addr = s.accept()
        print("HTTP client:", client_addr)
        http_server.handle_client(client)
    except OSError:
        pass  # Timeout - normal operation
    except Exception as e:
        print("HTTP: Unexpected error -", e)
        # Fortsæt loop, crash ikke

    # MQTT message handling
    try:
        if mqtt and mqtt.connected:
            mqtt.check_messages()
        elif mqtt and not mqtt.connected:
            mqtt_reconnect_timer += 1
            if mqtt_reconnect_timer > 30:
                mqtt_reconnect_timer = 0
                mqtt.reconnect()
    except Exception as e:
        print("MQTT: Loop error -", e)
        if mqtt:
            mqtt.connected = False
```

### Hvorfor?

- Fanger alle exceptions, ikke kun `OSError`
- MQTT-fejl isoleres fra HTTP-handling
- System fortsætter selv ved uventede fejl

---

## 1.4 Startup Fejlhåndtering

### Tilføj til main() funktionen

```python
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
        return  # Kan ikke fortsætte uden heater

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
        # Fortsæt alligevel - WiFi virker måske

    # ... resten som før
```

---

## Test Plan

Efter implementation, test følgende:

| Test | Forventet resultat |
|------|-------------------|
| Åbn `http://192.168.4.1/` | Normal response |
| Send malformed HTTP: `curl --raw -d "garbage" http://192.168.4.1/` | 400 Bad Request |
| Send til ukendt endpoint: `/asdf` | 404 Not Found |
| Tag WiFi-router fra strøm under drift | System fortsætter på AP |
| Send ikke-UTF8 bytes | 400 Bad Request |

---

## Implementeringsrækkefølge

```
Trin 1: Opdater http_server.py handle_client()
          ↓
Trin 2: Test HTTP fejlhåndtering
          ↓
Trin 3: Opdater main.py run_server_loop()
          ↓
Trin 4: Opdater main.py main()
          ↓
Trin 5: Upload til ESP32 og test
          ↓
Trin 6: Dokumenter i Engineering_Log.md
```

---

## Godkendelse

**Før jeg implementerer, bekræft venligst:**

- [ ] Jeg har læst og forstået ændringerne
- [ ] Jeg er klar til at teste på ESP32
- [ ] Start implementation

**Skriv "start" for at jeg begynder at ændre koden.**

---

*Ingen filer er ændret endnu. Dette dokument beskriver KUN hvad der vil blive ændret.*
