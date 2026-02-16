# TASK02: Implementation Plan - Fase 2: Fjern Global State

**Dato:** 2026-02-04
**Status:** Afventer godkendelse
**Fase:** 2 af 3
**Fokus:** Fjern global `_heater` variabel, brug dependency injection

---

## Baggrund

Fra TASK01_analysis.md:

> **Problem:** `http_server.py` bruger global `_heater` variabel.
> ```python
> _heater = None
> http_server._heater = heater  # Direkte adgang til modul-variabel
> ```
> **Konsekvens:** Tight coupling, svært at teste, None-reference risiko.

---

## Foreslået Løsning

Konverter `http_server.py` fra funktioner med global state til en klasse med eksplicit dependency injection.

---

## Nuværende Arkitektur

```
main.py
    │
    ├── heater = HeaterService()
    │
    └── http_server._heater = heater  ← Direkte modul-manipulation
            │
            └── _heater.turn_on()     ← Global variabel
```

---

## Ny Arkitektur

```
main.py
    │
    ├── heater = HeaterService()
    │
    └── server = HttpServer(heater)   ← Dependency injection
            │
            └── self.heater.turn_on() ← Instance variabel
```

---

## Implementation

### Ændring 1: http_server.py - Konverter til klasse

**Fra:**
```python
_heater = None

def turn_on(client):
    _heater.turn_on()
```

**Til:**
```python
class HttpServer:
    def __init__(self, heater):
        self.heater = heater
        self.socket = None

    def turn_on(self, client):
        self.heater.turn_on()
```

### Ændring 2: main.py - Brug klassen

**Fra:**
```python
http_server._heater = heater
http_server.handle_client(client)
```

**Til:**
```python
server = HttpServer(heater)
server.handle_client(client)
```

---

## Detaljeret Kodeændring

### http_server.py (ny struktur)

```python
class HttpServer:
    def __init__(self, heater):
        """Initialize HTTP server with heater service dependency."""
        self.heater = heater

    def handle_client(self, client):
        """Handle incoming HTTP request."""
        # ... parsing logic (unchanged) ...

        # Routing now uses self.heater
        if path == "/":
            self._index(client)
        elif path == "/status":
            self._status(client)
        elif path == "/on":
            self._turn_on(client)
        # ... etc

    def _index(self, client):
        body = "ESP32 Heater Controller..."
        self._send_response(client, 200, "OK", body)

    def _status(self, client):
        body = "Heater status: " + self.heater.status()
        self._send_response(client, 200, "OK", body)

    def _turn_on(self, client):
        self.heater.turn_on()
        body = "Heater turned ON"
        self._send_response(client, 200, "OK", body)

    def _send_response(self, client, code, text, body, content_type="text/plain"):
        # ... response logic ...
```

---

## Fordele ved Ændringen

| Aspekt | Før | Efter |
|--------|-----|-------|
| Kobling | Tight (global state) | Loose (dependency injection) |
| Testbarhed | Svær (kræver modul-manipulation) | Nem (inject mock) |
| Læsbarhed | Skjult afhængighed | Eksplicit afhængighed |
| Fejlrisiko | None-reference mulig | Fejl ved konstruktion |

---

## Risiko-vurdering

| Risiko | Sandsynlighed | Mitigation |
|--------|---------------|------------|
| Introduktion af bugs | Lav | Systematisk refactoring |
| Glemt at opdatere main.py | Lav | Test efter ændring |
| Sniffer-integration brydes | Mellem | Håndter sniffer separat |

**Note:** Sniffer-funktionaliteten bruger også en global `sniffer` instans. Den kan håndteres i en separat fase eller inkluderes her.

---

## Spørgsmål til dig

Før implementation:

1. **Skal sniffer også refaktoreres nu?**
   - Ja: Mere konsistent, men større ændring
   - Nej: Fokusér på heater først, sniffer senere

2. **Er du klar til at teste efter ændringen?**

---

## Godkendelse

Skriv `start` for at begynde implementation, eller stil spørgsmål først.
