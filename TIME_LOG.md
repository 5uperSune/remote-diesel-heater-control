# Time Log - Remote Diesel Heater Project

## Oversigt

| Uge | Timer | Akkumuleret |
|-----|-------|-------------|
| Uge 4 (jan) | 12 | 12 |
| Uge 5 (jan/feb) | 18 | 30 |
| Uge 6 (feb) | 10 | 40 |
| Uge 7 (feb) | 3 | 43 |

**Total estimeret: ~43 timer**

---

## Detaljeret log

### 2026-01-26 (Søndag)
| Aktivitet | Timer |
|-----------|-------|
| ESP32 indkøb og unboxing | 0.5 |
| Thonny IDE installation | 0.5 |
| MicroPython firmware download og flash | 1.0 |
| Boot-problem debugging (UART0 konflikt) | 2.0 |
| Recovery og re-flash | 1.0 |
| **Total** | **5.0** |

### 2026-01-27 (Mandag)
| Aktivitet | Timer |
|-----------|-------|
| UART2 loopback test setup | 1.5 |
| Verificering af GPIO pins | 1.0 |
| Research om Engineering Log praksis | 1.0 |
| Opsætning af log-struktur | 0.5 |
| **Total** | **4.0** |

### 2026-01-28 (Tirsdag)
| Aktivitet | Timer |
|-----------|-------|
| GitHub repository oprettelse | 0.5 |
| Git basics og første commits | 1.0 |
| Modularisering af kode (wifi_ap, http_server) | 1.5 |
| Test af modulær struktur | 0.5 |
| Dokumentation i Engineering Log | 0.5 |
| **Total** | **4.0** |

### 2026-02-03 (Mandag)
| Aktivitet | Timer |
|-----------|-------|
| Modulintegration debugging | 2.0 |
| HeaterService implementation | 1.0 |
| LED-statusindikatorer (GPIO18/19) | 1.5 |
| UART Sniffer modul | 2.0 |
| HTTP sniffer interface (HTML) | 2.0 |
| WiFi STA-mode implementation | 1.5 |
| MQTT client setup (HiveMQ) | 2.0 |
| Config-fil struktur | 0.5 |
| Engineering Log opdatering | 1.5 |
| **Total** | **14.0** |

### 2026-02-04 (Tirsdag)
| Aktivitet | Timer |
|-----------|-------|
| AGENT_TASK workflow setup | 1.0 |
| Kodeanalyse og review | 1.5 |
| Fase 1: Fejlhåndtering implementation | 2.0 |
| Fase 2: Dependency injection refactoring | 2.0 |
| Test af ændringer på ESP32 | 1.0 |
| Engineering Log dokumentation | 1.5 |
| Time log setup | 0.5 |
| **Total** | **9.5** |

### 2026-02-15 (Lørdag)
| Aktivitet | Timer |
|-----------|-------|
| WiFi-konfiguration til bådens netværk | 0.5 |
| Debugging af WiFi "Internal State Error" | 0.5 |
| Test af HTTP-interface på båden | 0.5 |
| UART Sniffer test med fjernbetjening | 1.0 |
| Debugging af sniffer stabilitetsproblemer | 0.5 |
| **Total** | **3.0** |

---

## Kategorier (til rapport)

| Kategori | Timer | % |
|----------|-------|---|
| Research & planlægning | 6 | 15% |
| Implementation | 18 | 45% |
| Test & debugging | 8 | 20% |
| Dokumentation | 8 | 20% |
| **Total** | **40** | 100% |

---

## Arbejdsmetode

- **AI-assisteret udvikling**: Ja (ChatGPT, Claude)
- **Pauser inkluderet**: Nej (kun aktiv arbejdstid)
- **Hardware-test**: Inkluderet i "Test & debugging"

### Reflektion over AI-assistance

AI-assistenten fungerede som en erfaren kollega der kunne:
- Forklare koncepter (UART, MQTT, MicroPython)
- Foreslå kodestruktur og arkitektur
- Debugge problemer hurtigere
- Skrive boilerplate-kode og dokumentation

Studenten var stadig ansvarlig for:
- Hardware-test og fysisk debugging
- Designbeslutninger og arkitekturvalg
- Forståelse af kode og koncepter
- Kvalitetssikring og test

**Estimeret tidsbesparelse med AI: 50-70%**

---

*Opdateret: 2026-02-04*
