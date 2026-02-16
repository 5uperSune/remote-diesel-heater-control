# TASK01: Architecture and Quality Analysis

**Dato:** 2026-02-03
**Status:** Analyse (afventer godkendelse)
**Baseret på:** AGENT_TASK.md

---

## 1. Nuværende Arkitektur

### 1.1 Fil-oversigt

| Fil | Linjer | Ansvar |
|-----|--------|--------|
| `main.py` | 112 | Opstart, orchestrering, main loop |
| `config.py` | 22 | Credentials og konfiguration |
| `wifi_ap.py` | 40 | Access Point mode |
| `wifi_sta.py` | 69 | Station mode (WiFi-forbindelse) |
| `mqtt_client.py` | 132 | MQTT fjernstyring |
| `http_server.py` | 341 | HTTP endpoints + HTML |
| `heater_service.py` | 49 | Forretningslogik + LED |
| `uart_sniffer.py` | 101 | Protokol reverse engineering |

**Total:** 866 linjer Python

### 1.2 Afhængighedsdiagram

```
config.py ◄──────────────────────────────────────┐
    │                                             │
    ├──► wifi_ap.py                               │
    ├──► wifi_sta.py                              │
    └──► mqtt_client.py ──► heater_service.py     │
                                   ▲              │
main.py ───┬──► wifi_ap.py         │              │
           ├──► wifi_sta.py        │              │
           ├──► mqtt_client.py ────┘              │
           └──► http_server.py ──► heater_service.py
                      │                           │
                      └──► uart_sniffer.py        │
                                                  │
config_example.py (template, ingen imports) ──────┘
```

### 1.3 Ansvarsfordeling

| Modul | Primært ansvar | Sekundære ansvar |
|-------|----------------|------------------|
| `main.py` | Opstart, lifecycle | Socket-håndtering, MQTT reconnect-logik |
| `heater_service.py` | State management | LED-kontrol |
| `http_server.py` | HTTP routing | HTML-generering, URL-parsing |
| `mqtt_client.py` | MQTT kommunikation | Command parsing |
| `uart_sniffer.py` | UART capture | Data formatting |

---

## 2. Identificerede Svagheder

### 2.1 KRITISK: Manglende fejlhåndtering

**Problem:** Flere steder kan exceptions crashe systemet.

| Fil | Linje | Problem |
|-----|-------|---------|
| `http_server.py` | 41 | `request_line.split()` crasher ved malformed request |
| `http_server.py` | 36 | `.decode()` crasher ved ikke-UTF8 data |
| `main.py` | 92-94 | `accept()` exception håndteres, men andre fejl ignoreres |
| `wifi_sta.py` | 32 | Ingen exception handling ved connect() |

**Konsekvens:** En enkelt malformed HTTP request kan crashe hele systemet.

**Prioritet:** 🔴 HØJ

---

### 2.2 HØJ: Global mutable state

**Problem:** `http_server.py` bruger global `_heater` variabel.

```python
# http_server.py linje 13
_heater = None

# main.py linje 84
http_server._heater = heater  # Direkte adgang til modul-variabel
```

**Konsekvens:**
- Tight coupling mellem main.py og http_server implementation
- Svært at teste isoleret
- Kan føre til None-reference errors

**Prioritet:** 🟠 MELLEM-HØJ

---

### 2.3 HØJ: http_server.py er en "god file"

**Problem:** Filen har 341 linjer og blander flere ansvar:
- HTTP routing (linje 34-76)
- HTML template generation (linje 141-210, 235-271)
- URL parsing (linje 220-226)
- Heater endpoints (linje 96-115)
- Sniffer endpoints (linje 120-336)

**Konsekvens:**
- Svært at vedligeholde
- HTML templates er hardcoded i Python
- Ændring af UI kræver ændring af Python-kode

**Prioritet:** 🟠 MELLEM-HØJ

---

### 2.4 MELLEM: Inkonsistent error reporting

**Problem:** Fejl rapporteres forskelligt:
- `print()` statements (de fleste steder)
- Return values (`connect_wifi` returnerer tuple)
- Exceptions (nogle steder fanges, andre ikke)

**Eksempel:**
```python
# wifi_sta.py - returnerer tuple
return False, None

# mqtt_client.py - returnerer bool
return False

# http_server.py - ingen error return, bare print
print("MQTT: Unknown command:", msg)
```

**Prioritet:** 🟡 MELLEM

---

### 2.5 MELLEM: Manglende input validation

**Problem:** HTTP endpoints validerer ikke input.

```python
# http_server.py linje 310
index = int(param[2:])  # Kan kaste ValueError
```

**Konsekvens:** Malformed requests kan give uventet adfærd.

**Prioritet:** 🟡 MELLEM

---

### 2.6 LAV: Magic numbers og hardcoded values

**Problem:** Flere hardcoded værdier spredt i koden:

| Fil | Linje | Værdi | Betydning |
|-----|-------|-------|-----------|
| `main.py` | 79 | `1.0` | Socket timeout |
| `main.py` | 105 | `30` | MQTT reconnect interval |
| `wifi_sta.py` | 14 | `20` | WiFi timeout default |
| `uart_sniffer.py` | 22 | `5000` | Capture duration |

**Prioritet:** 🟢 LAV

---

### 2.7 LAV: Ingen eksplicit state model

**Problem:** System-state er implicit fordelt:
- `heater._is_on` (heater state)
- `mqtt.connected` (connection state)
- `wifi_sta.is_connected()` (network state)

Der er ingen samlet "system status" der kan queries.

**Prioritet:** 🟢 LAV (men vigtig for fremtidig udvidelse)

---

## 3. Foreslåede Forbedringer

### 3.1 Prioriteret liste

| # | Forbedring | Prioritet | Kompleksitet | Påvirker filer |
|---|------------|-----------|--------------|----------------|
| 1 | Tilføj try/except i HTTP request parsing | 🔴 HØJ | Lav | http_server.py |
| 2 | Fjern global `_heater`, brug parameter | 🟠 MELLEM | Lav | http_server.py, main.py |
| 3 | Uddrag HTML templates til separat fil | 🟠 MELLEM | Mellem | http_server.py, (ny) templates.py |
| 4 | Opret central constants.py | 🟡 MELLEM | Lav | Alle filer |
| 5 | Tilføj input validation helpers | 🟡 MELLEM | Lav | http_server.py |
| 6 | Opret SystemState klasse | 🟢 LAV | Mellem | main.py, (ny) system_state.py |

---

### 3.2 Detaljerede forslag

#### Forslag 1: Robust HTTP parsing

**Nuværende kode (usikker):**
```python
def handle_client(client):
    try:
        request = client.recv(1024).decode()
        request_line = request.split("\r\n")[0]
        method, path, _ = request_line.split()  # CRASHER ved malformed!
```

**Foreslået kode (sikker):**
```python
def handle_client(client):
    try:
        request = client.recv(1024)
        if not request:
            return

        try:
            request = request.decode('utf-8')
        except UnicodeDecodeError:
            send_response(client, 400, "Bad Request", "Invalid encoding")
            return

        lines = request.split("\r\n")
        if not lines:
            send_response(client, 400, "Bad Request", "Empty request")
            return

        parts = lines[0].split()
        if len(parts) < 2:
            send_response(client, 400, "Bad Request", "Malformed request line")
            return

        method, path = parts[0], parts[1]
        # ... fortsæt med routing
```

**Begrundelse:** Forhindrer crash ved malformed requests.

---

#### Forslag 2: Dependency injection i stedet for global state

**Nuværende (problematisk):**
```python
# http_server.py
_heater = None

def turn_on(client):
    _heater.turn_on()  # Afhænger af global state
```

**Foreslået (cleaner):**
```python
# http_server.py
class HttpServer:
    def __init__(self, heater):
        self.heater = heater

    def turn_on(self, client):
        self.heater.turn_on()
```

**Begrundelse:**
- Eksplicit afhængighed
- Testbart med mock
- Ingen skjult kobling

---

#### Forslag 3: Separer HTML templates

**Nuværende:** 100+ linjer HTML embedded i Python-strenge.

**Foreslået struktur:**
```
templates/
├── sniffer.html
├── capture_result.html
└── base.html (optional)
```

**Alternativ (enklere):** `templates.py` med HTML som konstanter:
```python
# templates.py
SNIFFER_PAGE = """<!DOCTYPE html>..."""
CAPTURE_RESULT = """<!DOCTYPE html>..."""
```

**Begrundelse:**
- Adskiller presentation fra logik
- Nemmere at redigere HTML
- Følger MVC-princippet

---

## 4. Anbefalet Implementeringsrækkefølge

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: Stabilitet (skal gøres først)                      │
│  ─────────────────────────────────────                      │
│  1. Tilføj fejlhåndtering i http_server.py                  │
│  2. Tilføj fejlhåndtering i main.py server loop             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  FASE 2: Struktur (kan vente til stabilitet er på plads)    │
│  ────────────────────────────────────────────────────────   │
│  3. Fjern global _heater state                              │
│  4. Opret constants.py                                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  FASE 3: Vedligeholdelse (nice-to-have)                     │
│  ───────────────────────────────────────                    │
│  5. Uddrag HTML templates                                   │
│  6. Opret SystemState klasse                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Konklusion

Kodebasen er **funktionel og velstruktureret** for et embedded projekt. De vigtigste forbedringer handler om **robusthed**:

| Kategori | Nuværende | Mål |
|----------|-----------|-----|
| Sikkerhed | Kan crashe ved malformed input | Graceful error handling |
| Modularitet | God, men http_server.py er for stor | Bedre separation |
| Vedligeholdelse | Acceptabel | Templates adskilt fra logik |

**Anbefaling:** Start med Fase 1 (fejlhåndtering) da dette har højest impact på systemets pålidelighed.

---

## 6. Næste Skridt

Når du har læst denne analyse:

1. **Godkend** eller **kommenter** forslagene
2. Vælg hvilken fase vi skal starte med
3. Jeg opretter `TASK01_implementation.md` med konkret kode

**Spørgsmål til dig:**
- Er der forslag du er uenig i?
- Er der andre bekymringer du har om koden?
- Vil du starte med Fase 1?

---

*Denne analyse er read-only som specificeret i AGENT_TASK.md. Ingen filer er ændret.*
