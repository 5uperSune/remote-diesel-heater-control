INDHOLDSFORTEGNELSE:

Dato	Emne	Relevans
26/01 2026   	ESP32 recovery	Hardware setup
27/01 2026	UART loopback	Communication
28/01 2026  Oprette GitHub
03/02 2026	Modulintegration og HeaterService	Software arkitektur, refaktorering
03/02 2026	LED-statusindikatorer	Hardware integration, GPIO
03/02 2026	UART Sniffer med web-interface	Reverse engineering, protokolanalyse
03/02 2026	Internet-forbindelse og MQTT fjernstyring	Netværk, IoT, sikkerhed
04/02 2026	TASK01 Fase 1: Fejlhåndtering og robusthed	Software kvalitet, defensive programming
04/02 2026	TASK02 Fase 2: Dependency injection	Arkitektur, loose coupling
15/02 2026	WiFi-konfiguration på båden + Sniffer test	Netværk, hardware debugging


SKABELON:
Engineering Log – YYYY-MM-DD

Titel: Kort beskrivelse af sessionen

Kontekst
(Hvor og under hvilke omstændigheder blev der arbejdet?)

Mål for sessionen
(Hvad var hensigten med denne arbejdssession?)

Setup / Forudsætninger
(Hardware, software, versioner, pins, netværk osv.)

Observationer
(Hvad blev gjort, og hvad blev observeret – uden vurdering.)

Problem / Spørgsmål
(Hvad virkede ikke? Hvad krævede afklaring?)

Hypotese / Analyse
(Hvorfor tror jeg, dette skete?)

Beslutning
(Hvad blev besluttet – og evt. hvad blev bevidst fravalgt?)

Resultat
(Hvad blev udfaldet?)

Konsekvens / Læring
(Hvad betyder dette for projektets videre retning?)

Kode / Output / Referencer
(Kode, output, links, noter)



Engineering Log – ESP32 setup og recovery 26/01-2026
Dato: 2025-02-01


Titel: Initial ESP32 setup, flash-problem og recovery
Kontekst
Indledende projektfase. Fokus på klargøring af ESP32 og udviklingsmiljø. Ingen ekstern hardware (heater) tilsluttet.
Mål for sessionen
Installere udviklingsmiljø
Installere MicroPython på ESP32
Forberede platformen til videre tests

Setup / Forudsætninger
Hardware: ESP32 med Wi-Fi
IDE: Thonny
Dokumentation: SunFounder ESP32 Starter Kit
PC: Windows (COM-port identificeret via Enhedshåndtering)

Observationer
ESP32 blev indkøbt
Thonny IDE blev installeret
MicroPython firmware blev downloadet
MicroPython blev installeret på ESP32 i henhold til dokumentationen
Efterfølgende blev et testscript afviklet for at verificere pin-identifikation, hvor en jumperwire blev sat mellem RX og TX.

Problem / Spørgsmål
ESP32 kunne ikke afbryde et hurtigt kørende loop (CTRL+C virkede ikke).
Forsøg på at flashe enheden mislykkedes, og ESP32 kunne ikke bringes i korrekt download-mode.

Hypotese / Analyse
Jumperwiren mellem RX og TX belastede UART0 under boot. UART0 anvendes både til USB-kommunikation og bootstrapping, hvilket forhindrede korrekt flash.

Beslutning
Fjerne jumperwiren mellem RX og TX
Identificere korrekt COM-port
Foretage fuld flash-reset og geninstallere MicroPython

Resultat
ESP32 kunne flashes korrekt efter fjernelse af jumperwiren ved brug af:
python -m esptool --chip esp32 --port COM3 erase_flash
python -m esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-2024xxxx-v1.xx.bin

Konsekvens / Læring
UART0 (RX/TX-pins øverst på boardet) må aldrig belastes elektrisk under boot eller flash. Fremadrettet skal al ekstern seriel kommunikation benytte UART2.

________________________________________
Engineering Log – ESP32 setup og recovery  27/01-2026
Dato: 2025-02-01
Titel: Initial ESP32 setup, flash-problem og recovery

Kontekst
Indledende projektfase. Fokus på klargøring af ESP32 og udviklingsmiljø. Ingen ekstern hardware (heater) tilsluttet.
Mål for sessionen
•	Installere udviklingsmiljø
•	Installere MicroPython på ESP32
•	Forberede platformen til videre tests

Setup / Forudsætninger
•	Hardware: ESP32 med Wi-Fi
•	IDE: Thonny
•	Dokumentation: SunFounder ESP32 Starter Kit
•	PC: Windows (COM-port identificeret via Enhedshåndtering)

Observationer
•	ESP32 blev indkøbt
•	Thonny IDE blev installeret
•	MicroPython firmware blev downloadet
•	MicroPython blev installeret på ESP32 i henhold til dokumentationen
Efterfølgende blev et testscript afviklet for at verificere pin-identifikation, hvor en jumperwire blev sat mellem RX og TX.

Problem / Spørgsmål
ESP32 kunne ikke afbryde et hurtigt kørende loop (CTRL+C virkede ikke).
Forsøg på at flashe enheden mislykkedes, og ESP32 kunne ikke bringes i korrekt download-mode.
Hypotese / Analyse
Jumperwiren mellem RX og TX belastede UART0 under boot. UART0 anvendes både til USB-kommunikation og bootstrapping, hvilket forhindrede korrekt flash.

Beslutning
•	Fjerne jumperwiren mellem RX og TX
•	Identificere korrekt COM-port
•	Foretage fuld flash-reset og geninstallere MicroPython

Resultat
ESP32 kunne flashes korrekt efter fjernelse af jumperwiren ved brug af:
python -m esptool --chip esp32 --port COM3 erase_flash
python -m esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-2024xxxx-v1.xx.bin

Konsekvens / Læring
UART0 (RX/TX-pins øverst på boardet) må aldrig belastes elektrisk under boot eller flash. Fremadrettet skal al ekstern seriel kommunikation benytte UART2.
________________________________________




Engineering Log – UART2 loopback-test (RX/TX-verifikation)
Dato: 2025-02-01
Titel: Verifikation af UART2 RX/TX og GPIO-pin-identifikation
Kontekst
ESP32 var nyinstalleret med MicroPython og fungerede stabilt efter recovery.
Mål for sessionen
Verificere korrekt konfiguration af RX og TX på udvalgte GPIO-pins ved hjælp af en loopback-test.

Setup / Forudsætninger
•	Board: ESP32
•	Firmware: MicroPython v1.27.1
•	UART: UART2
•	GPIO: TX = GPIO17, RX = GPIO16
•	Fysisk loopback via jumperwire mellem GPIO17 og GPIO16

Observationer
En loopback-test blev udført, hvor data sendt på TX blev læst tilbage på RX. Alle sendte datapakker blev korrekt modtaget.
Hypotese / Analyse
Succesfuld loopback indikerer korrekt hardwareforbindelse og korrekt softwarekonfiguration af UART2.
Beslutning
Anvende UART2 (GPIO16/17) til al ekstern seriel kommunikation i projektet.
Resultat
10 ud af 10 datapakker blev korrekt modtaget.
UART2 loopback test on ESP32
TX = 17 RX = 16
OK: b'PING 0\n'
...
OK: b'PING 9\n'

Konsekvens / Læring
UART2 er bekræftet funktionsdygtig og kan anvendes som stabil kommunikationskanal til videre arbejde med seriel protokol-analyse og fjernstyring.


Engineering Log – 2026-01-27

Titel: Setup af Engineering Log

Kontekst
Rod i notaterne afstedgjorde at der måtte laves et Engineering Log-system

Mål for sessionen
Diskussion med ChatGPT om hvordan Log-systemer laves i branchen.

Setup / Forudsætninger
Word vs LaTeX. GitHub og formater deri.

Observationer
I GitHub giver det mening at gemme i .txt eller .md filer.

Problem / Spørgsmål
Det blev diskuteret hvilke programmer jeg foretrak og hvilke fordele vs ulemper der er ved de forskellige filer og programmer. 

Hypotese / Analyse

Beslutning
Jeg vil bruge Word til at skrive opgaven i da det giver mig en bedre skriveoplevelse. 
Desuden vil der i GitHub blive lavet en .md fil med Engineering Log. Denne fil vil løbende blive tilført Logs der beskriver, problemstillingerne, tankegangen, udfordringerne og løsningerne.
Der vil ligeledes blive lavet en skabelon øverst i Engineering Loggen der kan kopieres nederst i dokumentet så forløbet bliver beskrevet i et format der er kontinuerligt og overskueligt.
Til sidst blev det besluttet at lave en indholdsfortegnelse aller øverst i Engineering Loggen så man let kan se hvad der er blevet arbejdet med.

Resultat
https://github.com/5uperSune/remote-diesel-heater-control/new/main

Konsekvens / Læring
GitHub oprettet.

Kode / Output / Referencer
(https://github.com/5uperSune/remote-diesel-heater-control/new/main)



God og **meget vigtig pointe** — og du har helt ret:
det **skal** med i Engineering Log, fordi det viser, at du forstår **begrænsningerne** i løsningen, ikke kun succesen.

Her er en **revideret version**, hvor den diskussion er flettet ind **akademisk korrekt** (uden at blive lang eller uklar).
Du kan erstatte **Hypotese / Analyse** og **Beslutning** med nedenstående eller indsætte dem som udvidelse.

---

Tilføjelse / udvidelse til Engineering Log – 2026-01-28**

### **Hypotese / Analyse (revideret)**

Ved konfiguration af ESP32 i Access Point-mode etableres et isoleret, lokalt netværk (intranet), hvor al kommunikation foregår direkte mellem klient og ESP32.
Denne arkitektur giver deterministisk og robust adgang, men indebærer samtidig den væsentlige begrænsning, at ESP32 **ikke er tilgængelig via det offentlige internet (WWW)** og ikke kan nås udefra uden direkte Wi-Fi-forbindelse.

AP-mode er derfor velegnet til:

* lokal konfiguration
* fejlfinding
* fallback-adgang
* headless udvikling

men **ikke** til fjernadgang over længere afstande.

For at opnå adgang over internettet kræves en supplerende netværksarkitektur, fx:

* STA-mode (ESP32 som klient på eksisterende router)
* AP+STA kombination
* ekstern kommunikationskanal (fx GSM/LTE)

---

### **Observationer (supplerende)**

* Kommunikation via AP-mode fungerer udelukkende inden for ESP32’s lokale netværk (`192.168.4.0/24`)
* Enheder uden direkte forbindelse til ESP32’s Wi-Fi kan ikke tilgå systemet
* ESP32 fungerer ikke som gateway til internettet i AP-mode

---

### **Resultat af koden (præcisering)**

Den implementerede AP-løsning muliggør lokal HTTP-kommunikation, men giver **ingen ekstern netværksadgang**.
Dette bekræfter, at AP-mode alene ikke opfylder kravet om fjernstyring over internettet, men fungerer som en lokal kontrol- og servicegrænseflade.

---

### **Beslutning (revideret)**

* AP-mode anvendes som:

  * lokal konfigurations- og serviceadgang
  * fallback-løsning ved netværksfejl
* For egentlig fjernstyring kræves yderligere arkitektur:

  * ESP32 i STA-mode via eksisterende netværk
  * eller AP+STA kombination
  * alternativt GSM-baseret kommunikation
* Projektet fortsætter med fokus på:

  * lokal API-definition (HTTP)
  * state-model og logik
  * senere udvidelse med ekstern adgang som selvstændigt delmål


Engineering Log – 2026-01-28
Titel:
Modularisering af applikationen og etablering af versionsstyring (GitHub)
________________________________________
Kontekst
Efter etablering af stabil Wi-Fi Access Point-funktionalitet opstod behov for at strukturere koden mere modulært.
Projektet bevæger sig fra eksperimentel prototyping mod en mere vedligeholdelsesvenlig og rapport-egnet softwarearkitektur, i overensstemmelse med principper fra Software Engineering-undervisningen.
________________________________________
Mål for sessionen
•	Opdele applikationen i klart adskilte moduler
•	Etablere main.py som entydigt entry point
•	Isolere netværks- og transportlogik fra domænelogik
•	Uploade kildekoden til GitHub for versionsstyring
________________________________________
Setup / Forudsætninger
•	ESP32 med MicroPython v1.27
•	Udviklingsmiljø: VS Code / PyCharm
•	Test og upload til ESP via Thonny / mpremote
•	GitHub repository oprettet til projektet
•	Grundlæggende funktionel Wi-Fi AP og HTTP-kommunikation
________________________________________
Observationer
•	Tidligere funktionalitet var samlet i én fil, hvilket reducerede overblik
•	MicroPython eksekverer automatisk main.py ved boot
•	En tydelig opdeling i ansvar forbedrer både testbarhed og dokumentation
•	GitHub muliggør sporbarhed af ændringer og versionshistorik
________________________________________
Problem / Spørgsmål
•	Hvordan struktureres projektet, så hver komponent har ét klart ansvar?
•	Hvordan sikres et professionelt workflow mellem lokal udvikling, embedded deployment og versionsstyring?
________________________________________
Hypotese / Analyse
Ved at opdele koden i separate moduler opnås:
•	Separation of concerns
•	En tynd main.py, der udelukkende orkestrerer opstart
•	Genbrugelige og testbare komponenter
Versionsstyring via GitHub vurderes som nødvendig for:
•	dokumentation af udviklingsproces
•	rollback ved fejl
•	professionel afleveringskvalitet
________________________________________
Resultat af koden
Applikationen er opdelt i følgende filer:
•	main.py
o	Projektets entry point
o	Starter Wi-Fi AP og HTTP-server
o	Fungerer som orchestrator uden forretningslogik
•	wifi_ap.py
o	Indeholder al logik relateret til Wi-Fi Access Point
o	Initialiserer AP og netværkskonfiguration
o	Kan testes uafhængigt af resten af systemet
•	http_server.py
o	Indeholder simpel HTTP-server baseret på sockets
o	Håndterer routing og endpoints
o	Danner grundlag for senere /status, /on, /off funktionalitet
Kildekoden er efterfølgende:
•	committed lokalt
•	pushed til GitHub repository
Dette etablerer en klar “source of truth” for projektet.
________________________________________
Beslutning
•	Den modulære struktur fastholdes fremadrettet
•	main.py anvendes udelukkende til opstart og recovery
•	Videre udvikling sker i dedikerede moduler
•	GitHub anvendes konsekvent til versionsstyring og dokumentation
________________________________________


Engineering Log – 2026-02-03
Titel: Modulintegration, HeaterService-implementering og deployment via mpremote
________________________________________

Kontekst

Projektet havde på dette tidspunkt en planlagt modulær arkitektur, hvor `main.py` fungerede som orchestrator og importerede funktionalitet fra separate moduler. Imidlertid var der opstået en diskrepans mellem den arkitektur, som `main.py` forventede, og den faktiske implementation i de øvrige filer.

Sessionen blev udført i samarbejde med Claude Code (AI-assistent) som værktøj til kodeanalyse, refaktorering og deployment.

________________________________________

Mål for sessionen

• Identificere hvorfor den modulære arkitektur ikke fungerede
• Analysere hver Python-fil og kortlægge uoverensstemmelser
• Implementere de manglende komponenter
• Refaktorere eksisterende moduler så de matcher den planlagte arkitektur
• Deploye den fungerende løsning til ESP32
• Dokumentere processen i henhold til software engineering-praksis

________________________________________

Setup / Forudsætninger

• Hardware: ESP32 (NodeMCU ESP-32S) forbundet via USB (COM3)
• Firmware: MicroPython v1.27
• Udviklingsmiljø: Windows, Python 3.13, Thonny
• Deployment-værktøj: mpremote (installeret under sessionen)
• Eksisterende filer ved sessionens start:
  - main.py (orchestrator)
  - wifi_ap.py (standalone script)
  - http_server.py (delvist implementeret)
  - heater_service.py (MANGLEDE)

________________________________________

Observationer

Ved systematisk gennemgang af kodebasen blev følgende observeret:

**Observation 1: main.py forventede en specifik modulstruktur**

main.py indeholdt følgende imports og kald:
```python
from wifi_ap import start_ap
from http_server import start_server
from heater_service import HeaterService

def main():
    wlan = start_ap()
    heater = HeaterService()
    start_server(heater)
```

Dette indikerer en klar arkitektonisk intention:
- `wifi_ap` skal eksportere en `start_ap()` funktion der returnerer et WLAN-objekt
- `http_server` skal have en `start_server(heater)` funktion der accepterer en service-instans
- `heater_service` skal indeholde en `HeaterService` klasse

**Observation 2: wifi_ap.py var et standalone script, ikke et modul**

Den eksisterende `wifi_ap.py` indeholdt:
- Kode der eksekveres ved import (module-level execution)
- En abort-mekanisme via GPIO0 (boot-knap)
- En komplet HTTP-server implementeret inline
- Ingen funktioner at importere

Dette er et eksempel på "script-orienteret" programmering, som ikke understøtter genbrug eller modularitet.

**Observation 3: http_server.py matchede ikke main.py's forventninger**

Funktionen `start_server()` var defineret uden parametre:
```python
def start_server():  # Ingen parameter
```

Men main.py kaldte:
```python
start_server(heater)  # Forventer HeaterService-instans
```

Derudover var `/status` endpoint hardcoded:
```python
body = "Heater status: OFF"  # Statisk værdi, ikke fra service
```

**Observation 4: heater_service.py eksisterede ikke**

Filen var refereret i main.py men var aldrig blevet oprettet. Dette ville resultere i en `ImportError` ved runtime.

________________________________________

Problem / Spørgsmål

1. Hvorfor fejler programmet ved opstart?
   - ImportError: heater_service.py mangler
   - ImportError: wifi_ap.py har ingen `start_ap` funktion
   - TypeError: `start_server()` accepterer ikke argumenter

2. Hvordan bringes kodebasen i overensstemmelse med den planlagte arkitektur?

3. Hvilke software engineering-principper bør anvendes i refaktoreringen?

________________________________________

Hypotese / Analyse

**Årsagsanalyse**

Diskrepansen skyldes sandsynligvis en iterativ udviklingsproces, hvor:
1. Først blev et fungerende proof-of-concept skrevet som et enkelt script (wifi_ap.py med inline server)
2. Derefter blev en modulær arkitektur planlagt og dokumenteret i main.py
3. De individuelle moduler blev ikke fuldt opdateret til at matche den nye arkitektur

Dette er et klassisk eksempel på "technical debt" – hvor hurtige løsninger akkumulerer og skaber vedligeholdelsesproblemer.

**Software Engineering-principper anvendt i analysen**

*Separation of Concerns (SoC)*
Hvert modul bør have ét veldefineret ansvarsområde:
- wifi_ap.py: Netværkskonfiguration (Wi-Fi AP)
- http_server.py: HTTP-protokol og routing
- heater_service.py: Forretningslogik (heater state management)
- main.py: Systemorkestrering og lifecycle management

*Single Responsibility Principle (SRP)*
En klasse eller et modul bør kun have én grund til at ændre sig. Den originale wifi_ap.py havde flere ansvarsområder (Wi-Fi, HTTP, abort-logik), hvilket overtræder SRP.

*Dependency Injection (DI)*
Ved at lade `start_server()` modtage en `HeaterService`-instans som parameter opnås:
- Løs kobling mellem HTTP-laget og forretningslogikken
- Mulighed for at teste HTTP-serveren med mock-objekter
- Fleksibilitet til at udskifte HeaterService-implementationen

*Interface Segregation*
HeaterService eksponerer kun de metoder, som HTTP-serveren har brug for (`turn_on()`, `turn_off()`, `status()`), ikke interne implementationsdetaljer.

________________________________________

Beslutning

Følgende refaktoreringsplan blev besluttet og implementeret:

**1. Opret heater_service.py med HeaterService-klasse**

En simpel service-klasse der:
- Holder intern state (`_is_on`)
- Eksponerer metoder til at ændre og aflæse state
- Senere kan udvides med UART-kommunikation til fysisk heater

**2. Refaktorer wifi_ap.py til et importerbart modul**

- Fjern al module-level kode (kode der kører ved import)
- Opret `start_ap()` funktion der returnerer WLAN-objektet
- Fjern den inline HTTP-server (hører til http_server.py)
- Bevar konfigurationsparametre som modul-konstanter

**3. Opdater http_server.py til at acceptere dependency injection**

- Ændre `start_server()` til at acceptere en HeaterService-instans
- Opdater endpoints til at bruge den injicerede service
- Tilføj `/on` og `/off` endpoints for komplet funktionalitet
- Implementer en hjælpefunktion `send_response()` for at reducere kodeduplikering (DRY-princippet)

**4. Bevar main.py uændret**

Da main.py allerede udtrykte den ønskede arkitektur, blev den ikke modificeret. Dette validerer at den arkitektoniske plan var korrekt – kun implementationen manglede.

**Fravalg**

- Abort-mekanismen via GPIO0 blev fjernet fra wifi_ap.py. Denne funktionalitet kan genimplementeres i main.py hvis ønsket, men hører ikke til i et netværksmodul.
- Rickroll-funktionaliteten i http_server.py blev erstattet med en informativ index-side.

________________________________________

Resultat

**heater_service.py (ny fil)**
```python
class HeaterService:
    def __init__(self):
        self._is_on = False

    def turn_on(self):
        self._is_on = True
        print("Heater: ON")

    def turn_off(self):
        self._is_on = False
        print("Heater: OFF")

    def is_on(self):
        return self._is_on

    def status(self):
        return "ON" if self._is_on else "OFF"
```

Klassen følger encapsulation-princippet ved at bruge en privat variabel (`_is_on`) og eksponere state gennem metoder.

**wifi_ap.py (refaktoreret)**
```python
import network
import time

AP_SSID = "ESP32-AP"
AP_PASSWORD = "12345678"

def start_ap(ssid=None, password=None):
    ssid = ssid or AP_SSID
    password = password or AP_PASSWORD

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password, authmode=3)

    time.sleep(1)
    ip = ap.ifconfig()[0]
    print("Wi-Fi AP started:", ssid)
    print("IP address:", ip)

    return ap
```

Funktionen anvender default parameters, hvilket giver fleksibilitet uden at bryde eksisterende kald.

**http_server.py (refaktoreret)**

Centrale ændringer:
- Global `_heater` variabel holder reference til injiceret service
- `start_server(heater)` gemmer referencen og starter serveren
- Nye endpoints: `/`, `/status`, `/on`, `/off`
- `send_response()` hjælpefunktion reducerer kodeduplikering
- `SO_REUSEADDR` socket-option tilføjet for at undgå "address already in use" fejl ved genstart

**Deployment**

Installation af mpremote:
```
pip install mpremote
```

Upload af alle filer til ESP32:
```
python -m mpremote connect COM3 cp main.py wifi_ap.py http_server.py heater_service.py :
```

Genstart af ESP32:
```
python -m mpremote connect COM3 reset
```

**Verificering**

Efter deployment kan systemet tilgås via:
- Wi-Fi: SSID "ESP32-AP", password "12345678"
- Endpoints:
  - http://192.168.4.1/ → Viser tilgængelige endpoints
  - http://192.168.4.1/status → Viser aktuel heater-status
  - http://192.168.4.1/on → Tænder heater (ændrer state)
  - http://192.168.4.1/off → Slukker heater (ændrer state)

________________________________________

Konsekvens / Læring

**Tekniske læringer**

1. *Modularitet kræver disciplin*: Det er ikke nok at planlægge en modulær arkitektur – hver fil skal aktivt implementeres til at understøtte den.

2. *main.py som kontrakt*: Ved at skrive main.py først som en "ønsket API" blev det tydeligt, hvad de andre moduler skulle levere. Dette er en form for "programming by contract" eller "API-first design".

3. *Dependency Injection muliggør testbarhed*: Ved at injicere HeaterService i HTTP-serveren kan serveren senere testes isoleret med en mock-service.

4. *mpremote som deployment-værktøj*: mpremote viste sig effektivt til batch-upload af filer, hurtigere end manuel upload via Thonny.

**Proceduremæssige læringer**

1. *Systematisk fejlfinding*: Ved at læse hver fil og sammenligne med forventningerne i main.py blev problemerne identificeret metodisk.

2. *Dokumentation af "hvorfor"*: Denne log dokumenterer ikke kun hvad der blev ændret, men også rationalet bag beslutningerne. Dette er værdifuldt for fremtidig vedligeholdelse og for at demonstrere forståelse over for vejleder.

**Fremtidigt arbejde**

- HeaterService skal udvides med UART-kommunikation til den fysiske heater-controller
- Fejlhåndtering bør tilføjes (try/except i HTTP-handlers)
- Overvej at tilføje STA-mode for internet-adgang
- Implementer persistens af heater-state (så state bevares ved genstart)

________________________________________

Kode / Output / Referencer

**Filstruktur efter refaktorering:**
```
remote-diesel-heater-sandbox/
├── main.py              # Entry point, orchestrator
├── wifi_ap.py           # Wi-Fi Access Point modul
├── http_server.py       # HTTP server med endpoints
├── heater_service.py    # Forretningslogik (NEW)
├── README.md
├── Engineering_Log.md
└── .gitignore
```

**Afhængighedsgraf:**
```
main.py
   ├── wifi_ap.start_ap() → WLAN
   ├── heater_service.HeaterService() → service instance
   └── http_server.start_server(heater) → blocking server loop
                └── uses HeaterService methods
```

**Anvendte software engineering-principper:**
- Separation of Concerns (SoC)
- Single Responsibility Principle (SRP)
- Dependency Injection (DI)
- Don't Repeat Yourself (DRY)
- Encapsulation

**Værktøjer anvendt:**
- Claude Code (AI-assistent til kodeanalyse og refaktorering)
- mpremote v1.27.0 (deployment til ESP32)
- Python 3.13 (Windows)

________________________________________


Engineering Log – 2026-02-03 (fortsat)
Titel: Implementering af LED-statusindikatorer for visuel feedback
________________________________________

Kontekst

Efter succesfuld implementering af den modulære softwarearkitektur manglede systemet visuel feedback om heater-status. Brugeren skal kunne se systemets tilstand uden at tilgå HTTP-endpoints.

________________________________________

Mål for sessionen

• Tilføje visuel indikation af heater-status via LED'er
• Vælge egnede GPIO-pins til LED-styring
• Integrere hardware-kontrol i den eksisterende HeaterService-klasse
• Bevare separation of concerns (LED-logik hører til i service-laget)

________________________________________

Setup / Forudsætninger

• Eksisterende fungerende system med HeaterService
• To LED'er: Grøn (ON-indikator), Rød (OFF-indikator)
• Modstande: 220Ω (strømbegrænsning for LED'er)
• ESP32 GPIO-pins tilgængelige

________________________________________

Observationer

**GPIO-pin valg på ESP32**

Ikke alle GPIO-pins på ESP32 er egnede til generel brug. Nogle pins har specielle funktioner:

| Pin | Funktion | Egnet til LED? |
|-----|----------|----------------|
| GPIO0 | Boot-knap, strapping pin | Nej |
| GPIO1 | UART0 TX (USB) | Nej |
| GPIO2 | Boot strapping, ofte onboard LED | Undgås |
| GPIO3 | UART0 RX (USB) | Nej |
| GPIO6-11 | Flash SPI | Nej |
| GPIO12 | Boot strapping | Undgås |
| GPIO15 | Boot strapping | Undgås |
| GPIO16-17 | UART2 (reserveret til heater) | Nej |
| GPIO18-19 | Frie, ingen special funktion | **Ja** |
| GPIO21-23 | Frie, ingen special funktion | Ja |

GPIO18 og GPIO19 blev valgt da de:
- Ikke har specielle boot-funktioner
- Ikke konflikter med UART0 (USB) eller UART2 (heater-kommunikation)
- Er fysisk placeret tæt på hinanden på boardet
- Understøtter standard digital output

________________________________________

Problem / Spørgsmål

1. Hvor i arkitekturen skal LED-kontrollen placeres?
2. Hvilke GPIO-pins er sikre at bruge?
3. Hvordan sikres korrekt initial tilstand ved opstart?

________________________________________

Hypotese / Analyse

**Arkitektonisk placering af LED-logik**

Der er flere mulige placeringer for LED-kontrollen:

*Mulighed A: I main.py*
- Fordel: Centraliseret kontrol
- Ulempe: Bryder separation of concerns; main.py skal kun orkestrere

*Mulighed B: I http_server.py (ved endpoint-kald)*
- Fordel: Tæt på brugerinteraktion
- Ulempe: HTTP-serveren bør ikke kende til hardware-detaljer

*Mulighed C: I heater_service.py*
- Fordel: LED-status er direkte koblet til heater-state
- Fordel: Encapsulation - servicen håndterer al state-relateret logik
- Fordel: Automatisk synkronisering mellem intern state og visuel feedback

**Valg: Mulighed C** - HeaterService er ansvarlig for heater-state, og LED'erne er en direkte repræsentation af denne state. Ved at placere LED-logikken i HeaterService sikres, at visuel feedback altid er synkroniseret med den faktiske state, uanset hvordan state ændres.

**Elektrisk dimensionering**

LED forward voltage: ~2V (rød), ~2.2V (grøn)
ESP32 GPIO output voltage: 3.3V
Ønsket LED-strøm: ~10mA (synlig, men ikke maksimal lysstyrke)

Modstandsberegning (Ohms lov):
```
R = (V_gpio - V_led) / I_led
R = (3.3V - 2V) / 0.01A = 130Ω (minimum)
```

220Ω vælges for sikkerhedsmargin og længere LED-levetid.

________________________________________

Beslutning

• GPIO18 bruges til grøn LED (ON-indikator)
• GPIO19 bruges til rød LED (OFF-indikator)
• LED-kontrol implementeres i HeaterService.__init__(), turn_on() og turn_off()
• Ved opstart: Rød LED tændes (heater starter i OFF-tilstand)
• Pin-konfiguration defineres som modul-konstanter for nem ændring

________________________________________

Resultat

**Opdateret heater_service.py:**
```python
from machine import Pin

# GPIO pin configuration
PIN_LED_GREEN = 18  # ON indicator
PIN_LED_RED = 19    # OFF indicator


class HeaterService:
    def __init__(self):
        self._is_on = False

        # Initialize LED pins as outputs
        self._led_green = Pin(PIN_LED_GREEN, Pin.OUT)
        self._led_red = Pin(PIN_LED_RED, Pin.OUT)

        # Set initial state: heater is OFF, so red LED on
        self._led_green.off()
        self._led_red.on()

    def turn_on(self):
        self._is_on = True
        self._led_green.on()
        self._led_red.off()
        print("Heater: ON")

    def turn_off(self):
        self._is_on = False
        self._led_green.off()
        self._led_red.on()
        print("Heater: OFF")

    def is_on(self):
        return self._is_on

    def status(self):
        return "ON" if self._is_on else "OFF"
```

**Kredsløbsdiagram:**
```
ESP32                    LED'er
┌─────────┐
│  GPIO18 │──────[220Ω]────[LED Grøn ►|]────┐
│         │                                  │
│  GPIO19 │──────[220Ω]────[LED Rød  ►|]────┤
│         │                                  │
│     GND │──────────────────────────────────┘
└─────────┘
```

**LED-opførsel:**
| Heater State | Grøn LED (GPIO18) | Rød LED (GPIO19) |
|--------------|-------------------|------------------|
| OFF (boot)   | Slukket           | Tændt            |
| ON           | Tændt             | Slukket          |
| OFF          | Slukket           | Tændt            |

**Deployment:**
```
python -m mpremote connect COM3 cp heater_service.py : + reset
```

**Test:**
Verificeret ved at tilgå `/on` og `/off` endpoints - LED'erne skifter korrekt.

________________________________________

Konsekvens / Læring

**Tekniske læringer**

1. *GPIO-pin valg kræver research*: ESP32 har mange pins med specielle funktioner. At vælge forkerte pins kan forårsage boot-problemer eller konflikter med anden funktionalitet.

2. *State og visuel feedback bør være tæt koblet*: Ved at placere LED-kontrol i samme klasse som state-management undgås risikoen for, at visuel feedback kommer ud af sync med faktisk state.

3. *Modul-konstanter for hardware-konfiguration*: Ved at definere pin-numre som konstanter øverst i filen er det let at ændre hardware-konfiguration uden at søge gennem koden.

**Hardware læringer**

1. *Strømbegrænsning er vigtig*: Uden modstand ville LED'en trække for meget strøm og potentielt beskadige både LED og GPIO-pin.

2. *Active-high vs active-low*: I denne implementation bruges active-high logik (pin.on() = LED lyser). Nogle designs bruger active-low, hvor LED'en er forbundet til VCC og GPIO sænker til GND.

**Arkitektoniske læringer**

HeaterService har nu to ansvarsområder:
1. State management (intern `_is_on` variabel)
2. Hardware I/O (LED-kontrol)

Dette kunne argumenteres at bryde Single Responsibility Principle. En alternativ arkitektur kunne introducere en `StatusIndicator`-klasse, som HeaterService bruger. For projektets nuværende kompleksitet vurderes den valgte løsning dog som passende - prematur abstraktion bør undgås.

________________________________________

Kode / Output / Referencer

**Pin-mapping reference:**
- GPIO18 → Grøn LED (ON)
- GPIO19 → Rød LED (OFF)

**Komponenter:**
- 2x LED (grøn + rød, 5mm standard)
- 2x 220Ω modstand (1/4W)
- Jumperwires

**Udvidet afhængighedsgraf:**
```
main.py
   └── heater_service.HeaterService()
           ├── _is_on (state)
           ├── _led_green (Pin GPIO18)
           └── _led_red (Pin GPIO19)
```

________________________________________


Engineering Log – 2026-02-03 (fortsat)
Titel: UART Sniffer med web-baseret interface til protokol reverse engineering
________________________________________

Kontekst

For at kunne styre den eksisterende dieselvarmer via ESP32 er det nødvendigt først at forstå kommunikationsprotokollen mellem den originale fjernbetjening og varmerens controller. Dette kræver et værktøj til at opfange og analysere den serielle kommunikation.

Sessionen fokuserede på at udvikle et brugervenligt sniffer-værktøj med web-interface, så protokolanalyse kan udføres uden behov for separat software eller terminal-adgang.

________________________________________

Mål for sessionen

• Udvikle et UART sniffer-modul til at opfange seriel kommunikation
• Skabe et web-baseret interface til at styre snifferen
• Muliggøre labeling af opfangede kommandoer (fx "ON", "Mountain mode")
• Understøtte forskellige baud rates da protokollen er ukendt
• Integrere snifferen i det eksisterende HTTP-server setup

________________________________________

Setup / Forudsætninger

• Eksisterende fungerende ESP32 med Wi-Fi AP og HTTP-server
• UART2 allerede verificeret funktionel (GPIO16=RX, GPIO17=TX)
• Ukendt baud rate på heater-protokollen
• Behov for at kunne associere opfanget data med specifikke fjernbetjenings-handlinger

________________________________________

Observationer

**Udfordringen ved protokol reverse engineering**

Ved reverse engineering af en ukendt seriel protokol står man over for flere udfordringer:

1. *Ukendt baud rate*: Kommunikationshastigheden er ukendt og skal identificeres
2. *Ukendt dataformat*: Protokollen kan være binær, ASCII, eller en kombination
3. *Korrelation*: Man skal kunne matche opfanget data med den handling der udløste det
4. *Timing*: Kommandoer sendes kun når brugeren aktiverer fjernbetjeningen

**Designovervejelser for interface**

Flere interface-muligheder blev overvejet:

| Mulighed | Fordele | Ulemper |
|----------|---------|---------|
| REPL kommandoer | Simpelt at implementere | Kræver terminal, ikke brugervenligt |
| Fysisk knap på ESP32 | Ingen ekstern enhed | Begrænset feedback, kompleks tilstandsmaskine |
| HTTP med prædefinerede knapper | Brugervenligt | Ufleksibelt - kender ikke alle kommandoer |
| HTTP med tekstfelt | Fleksibelt, brugervenligt | Kræver mere HTTP-parsing |

**Valg: HTTP med brugerdefineret tekstfelt**

Et fritekst-inputfelt giver maksimal fleksibilitet. Brugeren kan skrive præcis hvad de vil teste, inklusiv kommandoer der endnu ikke er kendte (fx "Unknown button 3" eller "Mountain mode").

________________________________________

Problem / Spørgsmål

1. Hvordan håndteres ukendte kommandoer som brugeren endnu ikke kender navnet på?
2. Hvordan sikres at opfangningen sker på det rigtige tidspunkt i forhold til fjernbetjeningens aktivering?
3. Hvordan præsenteres binær data på en forståelig måde i en browser?

________________________________________

Hypotese / Analyse

**Tidsbaseret capture-tilgang**

Ved at bruge en fast capture-periode (5 sekunder) efter brugerens klik opnås:
- Brugeren har tid til at aktivere fjernbetjeningen
- Capture-vinduet er kort nok til at isolere én kommando
- Ingen kompleks synkronisering nødvendig

**Fleksibel labeling**

Ved at bruge et fritekst-felt i stedet for prædefinerede knapper:
- Brugeren kan navngive kommandoer som de opdages
- Ukendte kommandoer kan labels som "Unknown 1", "Weird beep", etc.
- Senere kan labels opdateres når funktionen identificeres

**Data-repræsentation**

Opfanget data vises i flere formater:
- **HEX**: Primært format for protokolanalyse (fx "A5 03 01 00 FF")
- **ASCII**: Nyttigt hvis protokollen indeholder læsbar tekst
- **Byte count**: Hjælper med at identificere faste vs. variable pakkelængder

________________________________________

Beslutning

**Arkitektur**

To nye komponenter tilføjes:

1. `uart_sniffer.py` - Selvstændigt modul med sniffer-logik:
   - `UartSniffer` klasse med konfigurerbar baud rate
   - `capture(label, duration)` metode til tidsbaseret opfangning
   - Intern liste til at gemme alle captures med labels
   - Formaterings-metoder til HEX og ASCII visning

2. Udvidelse af `http_server.py` med sniffer-endpoints:
   - `/sniffer` - Hovedside med inputfelt og capture-liste
   - `/sniffer/capture?label=X` - Udfør capture med given label
   - `/sniffer/data` - Vis alle captures som plain text
   - `/sniffer/clear` - Ryd alle captures
   - `/sniffer/delete?i=X` - Slet specifik capture
   - `/sniffer/baud?b=X` - Skift baud rate

**User Experience flow**

1. Bruger åbner `http://192.168.4.1/sniffer` i browser
2. Bruger indtaster ønsket label (fx "Mountain mode")
3. Bruger klikker "Capture (5 sek)"
4. Bruger aktiverer fjernbetjeningen inden 5 sekunder
5. Resultat vises med HEX og ASCII data
6. Capture gemmes i liste for senere sammenligning

________________________________________

Resultat

**uart_sniffer.py:**
```python
from machine import UART
import time

PIN_RX = 16
PIN_TX = 17
DEFAULT_BAUD = 9600
CAPTURE_DURATION_MS = 5000

class UartSniffer:
    def __init__(self, baud=DEFAULT_BAUD):
        self.baud = baud
        self.uart = None
        self.captured_commands = []

    def set_baud(self, baud):
        self.baud = baud

    def capture(self, label, duration_ms=CAPTURE_DURATION_MS):
        self.uart = UART(2, baudrate=self.baud, rx=PIN_RX, tx=PIN_TX)
        self.uart.init(self.baud, bits=8, parity=None, stop=1)

        if self.uart.any():
            self.uart.read()  # Clear buffer

        all_data = bytearray()
        start_time = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
            if self.uart.any():
                chunk = self.uart.read()
                if chunk:
                    all_data.extend(chunk)
            time.sleep_ms(1)

        self.uart.deinit()

        result = {
            "label": label,
            "data": bytes(all_data),
            "baud": self.baud,
            "bytes": len(all_data)
        }
        self.captured_commands.append(result)
        return result

    def format_hex(self, data):
        return " ".join("{:02X}".format(b) for b in data)

    def format_ascii(self, data):
        return "".join(chr(b) if 32 <= b <= 126 else "." for b in data)

sniffer = UartSniffer()  # Global instance
```

**Web interface (tilføjet til http_server.py):**

Endpoints:
- `GET /sniffer` → HTML side med formular og capture-liste
- `GET /sniffer/capture?label=X` → Udfører 5-sekunders capture
- `GET /sniffer/baud?b=9600` → Skifter baud rate

HTML interface features:
- Tekstfelt til fritekst label-input
- "Capture (5 sek)" knap
- Tabel med alle captures (nummer, label, størrelse, HEX data)
- Links til at skifte baud rate (4800, 9600, 19200, 38400)
- Slet-funktion for individuelle captures
- "Ryd alle" funktion

**Hardware tilslutning til sniffing:**
```
Heater System                ESP32
┌──────────────┐           ┌─────────┐
│ Controller   │           │         │
│         TX ──┼───────────┼── GPIO16│ (RX)
│              │           │         │
│         GND ─┼───────────┼── GND   │
└──────────────┘           └─────────┘
```

Bemærk: Under sniffing forbindes kun RX (læsning). TX bruges ikke, da vi kun observerer kommunikation - ikke sender.

**Screenshot af interface (tekstuel):**
```
┌─────────────────────────────────────────────────┐
│ UART Sniffer                                    │
│                                                 │
│ Baud rate: 9600  [4800] [9600] [19200] [38400] │
│                                                 │
│ Hvad vil du capture?                           │
│ ┌─────────────────────────────────────────────┐│
│ │ Mountain mode                               ││
│ └─────────────────────────────────────────────┘│
│ [Capture (5 sek)]                              │
│                                                 │
│ Captures (3)                                    │
│ ┌───┬──────────────┬───────┬──────────────┬───┐│
│ │ # │ Label        │ Size  │ Data (HEX)   │   ││
│ ├───┼──────────────┼───────┼──────────────┼───┤│
│ │ 1 │ ON           │ 5 B   │ A5 03 01 00  │Slet│
│ │ 2 │ OFF          │ 5 B   │ A5 03 00 00  │Slet│
│ │ 3 │ Mountain mode│ 8 B   │ A5 06 02 01..│Slet│
│ └───┴──────────────┴───────┴──────────────┴───┘│
│                                                 │
│ [Opdater] [Ryd alle] [Tilbage til heater]      │
└─────────────────────────────────────────────────┘
```

________________________________________

Konsekvens / Læring

**Tekniske læringer**

1. *Web-baseret tooling på embedded devices*: Ved at bygge værktøjer med web-interface undgås behovet for specialiseret software på host-computeren. En smartphone med browser er tilstrækkelig.

2. *Fleksibilitet vs. forudsigelighed*: Et fritekst-felt giver mere fleksibilitet end prædefinerede knapper, men kræver at brugeren selv holder styr på konsistent navngivning.

3. *Tidsbaseret capture*: En fast capture-periode er simpel at implementere og forstå, men kræver at brugeren timer deres input korrekt. En alternativ "start/stop"-tilgang ville være mere præcis men også mere kompleks.

4. *URL-encoding i MicroPython*: Simpel URL-decoding (erstatning af `+` og `%20` med mellemrum) er tilstrækkelig for basic brug, men en fuld URL-decoder ville være nødvendig for specielle tegn.

**Metodiske læringer for reverse engineering**

1. *Systematisk tilgang*: Ved at capture hver kommando flere gange kan man verificere konsistens. Identiske captures indikerer statiske kommandoer; varierende captures kan indeholde sekvensnumre eller timestamps.

2. *Sammenligning*: Ved at sammenligne HEX-data for forskellige kommandoer kan man identificere:
   - Header bytes (ofte ens for alle kommandoer)
   - Kommando-identifikator (varierer mellem kommandotyper)
   - Payload (parametre)
   - Checksum (ofte sidste byte(s))

3. *Baud rate identifikation*: Hvis data ser "tilfældig" ud (mange 0xFF eller 0x00), er baud rate sandsynligvis forkert. Korrekt baud rate giver typisk mere struktureret data.

**Næste skridt i protokolanalyse**

Efter indsamling af captures:
1. Identificer fælles header/præfiks i alle kommandoer
2. Find kommando-byte der adskiller ON/OFF/etc.
3. Analyser eventuelle parametre (temperatur, hastighed)
4. Identificer checksum-algoritme hvis tilstede
5. Implementer kommandoer i HeaterService

________________________________________

Kode / Output / Referencer

**Filstruktur efter tilføjelse:**
```
remote-diesel-heater-sandbox/
├── main.py              # Entry point
├── wifi_ap.py           # Wi-Fi AP modul
├── http_server.py       # HTTP server (nu med sniffer endpoints)
├── heater_service.py    # Heater state + LED kontrol
├── uart_sniffer.py      # UART sniffer modul (NEW)
├── README.md
├── Engineering_Log.md
└── .gitignore
```

**Udvidet afhængighedsgraf:**
```
main.py
   ├── wifi_ap.start_ap()
   ├── heater_service.HeaterService()
   └── http_server.start_server(heater)
           ├── Heater endpoints: /, /status, /on, /off
           └── Sniffer endpoints: /sniffer, /sniffer/capture, ...
                   └── uart_sniffer.sniffer (global instance)
```

**URL endpoints oversigt:**
| Endpoint | Metode | Beskrivelse |
|----------|--------|-------------|
| `/sniffer` | GET | Hovedside med capture-formular |
| `/sniffer/capture?label=X` | GET | Capture med label X (5 sek) |
| `/sniffer/data` | GET | Alle captures som plain text |
| `/sniffer/clear` | GET | Slet alle captures |
| `/sniffer/delete?i=N` | GET | Slet capture nummer N |
| `/sniffer/baud?b=9600` | GET | Sæt baud rate |

________________________________________


Engineering Log – 2026-02-03 (fortsat)
Titel: Internet-forbindelse via WiFi STA-mode og MQTT fjernstyring med HiveMQ Cloud
________________________________________

Kontekst

Projektets næste fase kræver fjernstyring af varmeren fra anywhere i verden - ikke kun via lokal WiFi-forbindelse. Dette nødvendiggør:
1. ESP32 skal forbinde til internettet via eksisterende hjemmenetværk
2. En sikker kommunikationskanal til fjernstyring
3. Bevarelse af lokal adgang som fallback

Sessionen fokuserede på at implementere dual-mode netværk (STA+AP) og MQTT-baseret fjernstyring via HiveMQ Cloud.

________________________________________

Mål for sessionen

• Forbinde ESP32 til eksisterende WiFi-netværk (STA-mode)
• Bevare AP-mode som fallback ved netværksfejl
• Implementere MQTT-client til sikker fjernstyring
• Adskille credentials fra kode for sikkerhed og delebarhed
• Muliggøre at projektet let kan overdrages til andre (f.eks. nabo)

________________________________________

Setup / Forudsætninger

• Eksisterende fungerende system med HTTP-server og heater control
• HiveMQ Cloud konto (gratis tier)
• Hjemmenetværk med WPA2
• MicroPython med umqtt.simple bibliotek (inkluderet i standard firmware)

________________________________________

Observationer

**Netværksarkitektur-muligheder**

Tre hovedtilgange til internetforbindelse blev overvejet:

| Tilgang | Fordele | Ulemper |
|---------|---------|---------|
| Kun STA-mode | Simpelt | Ingen adgang hvis WiFi fejler |
| Kun AP-mode + port forwarding | Altid tilgængelig lokalt | Kompleks router-setup, sikkerhedsrisiko |
| AP+STA dual-mode | Bedste af begge verdener | Lidt mere kompleks kode |

**Valg: AP+STA dual-mode**

ESP32 understøtter samtidig drift af både AP og STA interfaces. Dette giver:
- Internet-adgang via hjemmenetværk (STA)
- Lokal fallback-adgang via direkte forbindelse (AP)
- Redundans ved netværksproblemer

**Kommunikationsprotokol-muligheder**

| Protokol | Fordele | Ulemper |
|----------|---------|---------|
| HTTP med port forwarding | Simpelt, kendt | Sikkerhedsrisiko, kræver statisk IP/DDNS |
| WebSocket | Realtime, bi-directional | Kompleks implementation |
| MQTT | Lightweight, IoT-standard, pub/sub | Kræver broker |

**Valg: MQTT med cloud broker**

MQTT (Message Queuing Telemetry Transport) er designet til IoT-enheder med begrænsede ressourcer:
- Minimal protokol-overhead
- Publish/subscribe-model (asynkron)
- QoS-niveauer for pålidelig levering
- TLS-kryptering for sikkerhed
- Cloud-broker eliminerer behov for port forwarding

**Sikkerhedsovervejelser**

Credentials (WiFi-password, MQTT-credentials) skal beskyttes:

1. *Ikke i versionskontrol*: Credentials må aldrig committes til GitHub
2. *Separat konfigurationsfil*: Nem at ændre, nem at dele template
3. *TLS-kryptering*: Al MQTT-trafik krypteres
4. *Autentificering*: MQTT-broker kræver brugernavn/password

**Udfordring: Credential-deling**

Brugeren ønskede at kunne overdrage projektet til en nabo, som skal bruge sine egne credentials. Løsning:
- `config.py` - Brugerens egne credentials (i .gitignore)
- `config_example.py` - Template med placeholder-værdier (på GitHub)

Naboen kopierer `config_example.py` til `config.py` og udfylder sine egne værdier.

________________________________________

Problem / Spørgsmål

1. Hvordan kombineres HTTP-server (blocking) med MQTT message checking?
2. Hvordan håndteres reconnection ved netværkstab?
3. Hvordan struktureres kode så credentials er adskilt fra logik?

________________________________________

Hypotese / Analyse

**Kombineret HTTP + MQTT loop**

Standard HTTP-server bruger blocking `accept()` som venter på forbindelser. Dette forhindrer MQTT message checking.

Løsning: Socket timeout
```python
s.settimeout(1.0)  # 1 sekund timeout
```

Med timeout returnerer `accept()` efter 1 sekund hvis ingen forbindelse modtages. Dette tillader MQTT checking mellem HTTP-requests:

```
Loop:
  ├── accept() med timeout (max 1 sek)
  │     ├── HTTP request → handle
  │     └── Timeout → fortsæt
  └── mqtt.check_msg() (non-blocking)
```

**Configuration pattern**

Ved at bruge Python-moduler til konfiguration opnås:
- Type-sikkerhed (strenge, integers)
- Ingen parsing-kode nødvendig
- IDE-support (autocomplete)
- Simpel import-syntaks

```python
# config.py
WIFI_SSID = "MyNetwork"
WIFI_PASSWORD = "secret123"

# wifi_sta.py
from config import WIFI_SSID, WIFI_PASSWORD
```

**MQTT topic-struktur**

Simpel hierarkisk struktur med device-ID som prefix:
```
heater1/
  ├── command   (subscribe - modtag kommandoer)
  └── status    (publish - send status)
```

Kommandoer: `on`, `off`, `status`
Status-svar: `ON`, `OFF`, `offline`

________________________________________

Beslutning

**1. Opret config-system:**
- `config.py` - Brugerens credentials (gitignored)
- `config_example.py` - Template til deling

**2. Implementer WiFi STA-modul (wifi_sta.py):**
- `connect_wifi(timeout)` - Forbind med timeout
- `is_connected()` - Check forbindelsesstatus
- `get_ip()` - Hent tildelt IP-adresse

**3. Implementer MQTT-client (mqtt_client.py):**
- `HeaterMQTT` klasse med dependency injection af HeaterService
- TLS-krypteret forbindelse til HiveMQ (port 8883)
- Automatisk status-publicering ved kommandoer
- Reconnection-logik ved forbindelsestab

**4. Opdater main.py med ny startup-sekvens:**
1. Initialiser HeaterService
2. Forbind til WiFi (STA)
3. Start AP (fallback)
4. Forbind til MQTT
5. Kør kombineret HTTP+MQTT loop

**5. Opdater wifi_ap.py til at bruge config**

________________________________________

Resultat

**config_example.py (template):**
```python
# WiFi Settings
WIFI_SSID = "YourWiFiName"
WIFI_PASSWORD = "YourWiFiPassword"

# MQTT Settings (HiveMQ Cloud)
MQTT_BROKER = "your-cluster.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "your-username"
MQTT_PASSWORD = "your-mqtt-password"
MQTT_TOPIC_PREFIX = "heater1"

# Access Point Settings (fallback)
AP_SSID = "ESP32-Heater"
AP_PASSWORD = "heater1234"
```

**wifi_sta.py:**
```python
import network
import time
from config import WIFI_SSID, WIFI_PASSWORD

def connect_wifi(timeout=20):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if sta.isconnected():
        return True, sta.ifconfig()[0]

    print("WiFi: Connecting to '{}'...".format(WIFI_SSID))
    sta.connect(WIFI_SSID, WIFI_PASSWORD)

    start = time.time()
    while not sta.isconnected():
        if time.time() - start > timeout:
            return False, None
        time.sleep(0.5)

    ip = sta.ifconfig()[0]
    print("WiFi: Connected! IP:", ip)
    return True, ip

def is_connected():
    return network.WLAN(network.STA_IF).isconnected()

def get_ip():
    sta = network.WLAN(network.STA_IF)
    return sta.ifconfig()[0] if sta.isconnected() else None
```

**mqtt_client.py (centrale dele):**
```python
from umqtt.simple import MQTTClient
import ssl
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPIC_PREFIX

TOPIC_COMMAND = MQTT_TOPIC_PREFIX + "/command"
TOPIC_STATUS = MQTT_TOPIC_PREFIX + "/status"

class HeaterMQTT:
    def __init__(self, heater_service):
        self.heater = heater_service
        self.client = None
        self.connected = False

    def connect(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.verify_mode = ssl.CERT_NONE

        self.client = MQTTClient(
            client_id,
            MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=ssl_context
        )
        self.client.set_callback(self._on_message)
        self.client.connect()
        self.client.subscribe(TOPIC_COMMAND)
        self.connected = True

    def _on_message(self, topic, msg):
        msg = msg.decode().strip().lower()
        if msg == "on":
            self.heater.turn_on()
            self.publish_status()
        elif msg == "off":
            self.heater.turn_off()
            self.publish_status()

    def publish_status(self):
        self.client.publish(TOPIC_STATUS, self.heater.status())

    def check_messages(self):
        self.client.check_msg()  # Non-blocking
```

**main.py startup-sekvens:**
```python
def main():
    print("ESP32 Heater Controller")

    # 1. Initialize heater service
    heater = HeaterService()

    # 2. Connect to WiFi (STA mode)
    wifi_ok, ip = connect_wifi(timeout=20)

    # 3. Start AP mode as fallback
    start_ap()

    # 4. Connect to MQTT (if WiFi connected)
    mqtt = None
    if wifi_ok:
        mqtt = HeaterMQTT(heater)
        mqtt.connect()

    # 5. Run combined HTTP + MQTT loop
    run_server_loop(heater, mqtt)
```

**Kombineret server loop:**
```python
def run_server_loop(heater, mqtt):
    s = socket.socket()
    s.bind(("0.0.0.0", 80))
    s.listen(1)
    s.settimeout(1.0)  # Non-blocking

    while True:
        try:
            client, addr = s.accept()
            http_server.handle_client(client)
        except OSError:
            pass  # Timeout - no request

        if mqtt and mqtt.connected:
            mqtt.check_messages()
```

**Arkitekturdiagram:**
```
                    ┌─────────────────────────────────────┐
                    │           INTERNET                  │
                    └─────────────┬───────────────────────┘
                                  │
                    ┌─────────────▼───────────────────────┐
                    │      HiveMQ Cloud Broker            │
                    │  (TLS krypteret, port 8883)         │
                    └─────────────┬───────────────────────┘
                                  │ MQTT
    ┌─────────────────────────────▼─────────────────────────────┐
    │                     HOME ROUTER                            │
    │                   (192.168.1.x)                            │
    └─────────────────────────────┬─────────────────────────────┘
                                  │ WiFi (STA)
                    ┌─────────────▼───────────────────────┐
                    │           ESP32                      │
                    │  ┌─────────────────────────────┐    │
                    │  │ STA: 192.168.1.x (fra DHCP) │    │
                    │  │ AP:  192.168.4.1 (fallback) │    │
                    │  └─────────────────────────────┘    │
                    │                                      │
                    │  HTTP Server (port 80)               │
                    │  MQTT Client → HiveMQ                │
                    │  HeaterService → LED + (UART)        │
                    └─────────────────────────────────────┘
                                  │ AP WiFi
                    ┌─────────────▼───────────────────────┐
                    │  Direct Client (fallback)            │
                    │  Smartphone/Laptop                   │
                    └─────────────────────────────────────┘
```

**Test med MQTT Explorer:**

For at teste fjernstyring kan en MQTT-client som "MQTT Explorer" bruges:
1. Opret forbindelse til HiveMQ broker
2. Subscribe til `heater1/status`
3. Publish til `heater1/command`:
   - `on` → Tænder heater, LED skifter til grøn
   - `off` → Slukker heater, LED skifter til rød
   - `status` → Returnerer nuværende status

________________________________________

Konsekvens / Læring

**Tekniske læringer**

1. *Dual-mode networking*: ESP32 kan køre STA og AP samtidigt. Dette giver redundans uden ekstra hardware.

2. *Non-blocking I/O*: Ved at bruge socket timeout kan en single-threaded applikation håndtere multiple I/O-kilder (HTTP + MQTT).

3. *Configuration as code*: Python-moduler som konfigurationsfiler giver type-sikkerhed og IDE-support uden parsing-overhead.

4. *MQTT QoS*: Default QoS 0 ("fire and forget") er tilstrækkelig for heater-kontrol. Kritiske applikationer bør overveje QoS 1 eller 2.

**Sikkerhedslæringer**

1. *Credential separation*: Ved at adskille credentials fra kode:
   - Kode kan deles frit (GitHub)
   - Credentials forbliver private
   - Andre kan nemt tilpasse til deres setup

2. *TLS er essensielt*: MQTT uden TLS sender credentials i klartekst. Port 8883 med TLS er standard for sikker MQTT.

3. *Principle of least privilege*: MQTT-brugeren bør kun have adgang til nødvendige topics (kan konfigureres i HiveMQ).

**Arkitektoniske læringer**

1. *Dependency Injection betaler sig*: Ved at lade HeaterMQTT modtage HeaterService som parameter:
   - MQTT-modulet er uafhængigt af heater-implementation
   - Samme HeaterService bruges af både HTTP og MQTT
   - Konsistent state uanset kontrolmetode

2. *Event-driven vs. polling*: MQTT `check_msg()` er polling-baseret. En event-driven tilgang med interrupts ville være mere effektiv, men også mere kompleks.

**Delbarhed og vedligeholdelse**

Projektet kan nu nemt overdrages:
1. Modtager kloner repository fra GitHub
2. Kopierer `config_example.py` til `config.py`
3. Udfylder egne credentials
4. Uploader til ESP32

Ingen kodeændringer nødvendige for at tilpasse til andet netværk.

________________________________________

Kode / Output / Referencer

**Filstruktur efter tilføjelse:**
```
remote-diesel-heater-sandbox/
├── main.py              # Entry point med dual-mode startup
├── config.py            # Credentials (GITIGNORED)
├── config_example.py    # Template til deling
├── wifi_ap.py           # AP-mode (fallback)
├── wifi_sta.py          # STA-mode (internet)
├── mqtt_client.py       # MQTT fjernstyring
├── http_server.py       # HTTP endpoints
├── heater_service.py    # Forretningslogik + LED
├── uart_sniffer.py      # Protokol reverse engineering
├── README.md
├── Engineering_Log.md
└── .gitignore           # Inkluderer config.py
```

**Udvidet afhængighedsgraf:**
```
config.py
   │
   ├──▶ wifi_sta.py (WIFI_SSID, WIFI_PASSWORD)
   ├──▶ wifi_ap.py (AP_SSID, AP_PASSWORD)
   └──▶ mqtt_client.py (MQTT_*)

main.py
   ├── wifi_sta.connect_wifi() → bool, IP
   ├── wifi_ap.start_ap() → WLAN
   ├── heater_service.HeaterService()
   ├── mqtt_client.HeaterMQTT(heater)
   │       ├── subscribe(heater1/command)
   │       └── publish(heater1/status)
   └── http_server (via run_server_loop)
```

**MQTT Topic reference:**
| Topic | Retning | Payload | Beskrivelse |
|-------|---------|---------|-------------|
| `heater1/command` | App → ESP32 | `on`, `off`, `status` | Kommandoer til heater |
| `heater1/status` | ESP32 → App | `ON`, `OFF`, `offline` | Status-opdateringer |

**HiveMQ Cloud setup-guide:**
1. Gå til https://www.hivemq.com/mqtt-cloud-broker/
2. Opret gratis konto
3. Opret nyt cluster (vælg "Free" tier)
4. Under "Access Management" → opret credentials
5. Notér:
   - Cluster URL (fx `abc123.s1.eu.hivemq.cloud`)
   - Username
   - Password
6. Indsæt i `config.py`

**Test-kommandoer med mosquitto_pub:**
```bash
# Tænd heater
mosquitto_pub -h abc123.s1.eu.hivemq.cloud -p 8883 \
  -u "user" -P "pass" --capath /etc/ssl/certs \
  -t "heater1/command" -m "on"

# Sluk heater
mosquitto_pub ... -t "heater1/command" -m "off"

# Få status
mosquitto_pub ... -t "heater1/command" -m "status"
```

________________________________________


Engineering Log – 2026-02-04
Titel: TASK01 Fase 1 - Implementering af fejlhåndtering og robusthed
________________________________________

Kontekst

Som del af en formaliseret software engineering workflow blev der udført en arkitektur- og kvalitetsanalyse af kodebasen (dokumenteret i AGENT_TASK.md og TASK01_analysis.md). Analysen identificerede flere svagheder relateret til fejlhåndtering og robusthed.

Denne session implementerer Fase 1 af de anbefalede forbedringer med fokus på defensive programming og graceful error handling.

________________________________________

Mål for sessionen

• Implementere robust HTTP request parsing der ikke crasher ved malformed input
• Tilføje exception handling i main server loop
• Sikre at systemet fortsætter drift selv ved uventede fejl
• Følge en professionel software engineering workflow med review og godkendelse

________________________________________

Setup / Forudsætninger

• Eksisterende funktionel kodebase
• AGENT_TASK.md med kvalitetskrav
• TASK01_analysis.md med identificerede svagheder
• TASK01_implementation.md med godkendt implementeringsplan

________________________________________

Observationer

**Identificerede svagheder (fra analyse):**

| Prioritet | Problem | Risiko |
|-----------|---------|--------|
| 🔴 HØJ | `request.decode()` kan kaste UnicodeDecodeError | System crash |
| 🔴 HØJ | `request_line.split()` fejler ved malformed requests | System crash |
| 🔴 HØJ | Kun `OSError` fanges i main loop | Andre exceptions crasher |
| 🟠 MELLEM | Ingen fejlhåndtering ved startup | Uklart fejlmode |

**Defensive Programming principper anvendt:**

1. *Fail gracefully*: Returner fejlbesked til client i stedet for crash
2. *Catch specific, then general*: Fang kendte exceptions først, derefter `Exception`
3. *Always close resources*: Brug `finally` til at sikre socket lukkes
4. *Log errors*: Print fejl til konsol for debugging

________________________________________

Problem / Spørgsmål

1. Hvordan håndteres malformed HTTP requests uden at crashe?
2. Hvordan sikres at én fejlende request ikke påvirker efterfølgende requests?
3. Hvordan balanceres mellem detaljeret fejlhåndtering og kode-kompleksitet?

________________________________________

Hypotese / Analyse

**Defense in Depth tilgang:**

Tre lag af fejlhåndtering implementeres:

```
┌─────────────────────────────────────────────────────────┐
│ Lag 1: Input Validation                                 │
│ - Check for tomme requests                              │
│ - Validér UTF-8 encoding                                │
│ - Validér request line format                           │
├─────────────────────────────────────────────────────────┤
│ Lag 2: Handler Exception Catching                       │
│ - Try/except omkring routing                            │
│ - 500 Internal Server Error ved uventede fejl           │
├─────────────────────────────────────────────────────────┤
│ Lag 3: Main Loop Protection                             │
│ - Catch all exceptions i server loop                    │
│ - Log fejl men fortsæt drift                            │
└─────────────────────────────────────────────────────────┘
```

**HTTP Status Codes anvendt:**

| Code | Betydning | Hvornår |
|------|-----------|---------|
| 400 | Bad Request | Malformed input, invalid encoding |
| 404 | Not Found | Ukendt endpoint |
| 500 | Internal Server Error | Uventet exception i handler |

________________________________________

Beslutning

Implementer følgende ændringer:

**1. http_server.py - handle_client():**
- Tilføj UnicodeDecodeError handling
- Validér request line har mindst 2 dele
- Wrap routing i try/except
- Sikr socket lukkes i finally (med try/except)

**2. main.py - main():**
- Wrap hver startup-fase i try/except
- FATAL error ved HeaterService fejl (kan ikke fortsætte)
- Non-fatal errors ved WiFi/AP/MQTT (fortsæt med reduceret funktionalitet)

**3. main.py - run_server_loop():**
- Fang alle exceptions, ikke kun OSError
- Isolér MQTT fejl fra HTTP handling
- Log fejl men fortsæt loop

________________________________________

Resultat

**http_server.py - Ny handle_client():**

```python
def handle_client(client):
    try:
        # 1. Receive raw data
        raw_request = client.recv(1024)
        if not raw_request:
            return

        # 2. Decode with error handling
        try:
            request = raw_request.decode('utf-8')
        except UnicodeDecodeError:
            print("HTTP: Invalid UTF-8 encoding")
            send_response(client, 400, "Bad Request", "Invalid encoding")
            return

        # 3. Parse request line safely
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

        # 4. Route with exception handling
        try:
            # ... routing logic ...
        except Exception as e:
            print("HTTP: Handler error -", e)
            try:
                send_response(client, 500, "Internal Server Error", "Server error")
            except:
                pass

    except Exception as e:
        print("HTTP: Request error -", e)

    finally:
        try:
            client.close()
        except:
            pass
```

**main.py - Ny startup med fejlhåndtering:**

```python
def main():
    # 1. Initialize heater service
    try:
        heater = HeaterService()
    except Exception as e:
        print("FATAL: HeaterService init failed -", e)
        return  # Cannot continue without heater

    # 2. Connect to WiFi
    wifi_ok = False
    ip = None
    try:
        wifi_ok, ip = connect_wifi(timeout=20)
    except Exception as e:
        print("WiFi: Connection error -", e)
        wifi_ok = False

    # 3. Start AP (continue even if fails)
    try:
        start_ap()
    except Exception as e:
        print("AP: Failed to start -", e)

    # 4. Connect MQTT
    mqtt = None
    if wifi_ok:
        try:
            mqtt = HeaterMQTT(heater)
            if not mqtt.connect():
                print("MQTT: Will retry later...")
        except Exception as e:
            print("MQTT: Init error -", e)
            mqtt = None
```

**main.py - Robust server loop:**

```python
while True:
    # HTTP handling
    try:
        client, client_addr = s.accept()
        http_server.handle_client(client)
    except OSError:
        pass  # Timeout - normal
    except Exception as e:
        print("HTTP: Unexpected error -", e)

    # MQTT handling (isolated from HTTP)
    try:
        if mqtt and mqtt.connected:
            mqtt.check_messages()
        elif mqtt and not mqtt.connected:
            # Reconnect logic...
    except Exception as e:
        print("MQTT: Loop error -", e)
        if mqtt:
            mqtt.connected = False
```

________________________________________

Konsekvens / Læring

**Tekniske læringer**

1. *Defensive programming er essensielt for embedded systems*: Uden proper fejlhåndtering kan en enkelt malformed request kræve fysisk genstart af enheden.

2. *Layered error handling*: Ved at have flere lag af fejlhåndtering sikres at fejl fanges på det mest specifikke niveau muligt.

3. *Fail-safe vs fail-secure*: Systemet er designet til at fortsætte drift (fail-safe) ved de fleste fejl, men stopper ved kritiske fejl (HeaterService init).

4. *Resource cleanup er kritisk*: `finally` blokke sikrer at sockets altid lukkes, selv ved exceptions.

**Proces-læringer**

1. *Formaliseret workflow virker*: Ved at følge AGENT_TASK → analyse → implementation → review flowet blev ændringerne velovervejet og dokumenteret.

2. *Inkrementel forbedring*: Ved at dele forbedringerne i faser (Fase 1: robusthed, Fase 2: struktur, Fase 3: vedligeholdelse) undgås "big bang" refactoring.

3. *Kode review før implementation*: Ved at skrive implementeringsplanen først og få godkendelse undgås spildt arbejde.

**Software Engineering principper demonstreret**

- Defensive Programming
- Defense in Depth
- Graceful Degradation
- Fail-Safe Design
- Resource Management (RAII-lignende med finally)

________________________________________

Kode / Output / Referencer

**Ændrede filer:**
- `http_server.py` - handle_client() med robust parsing
- `main.py` - main() og run_server_loop() med exception handling

**Workflow dokumenter:**
- `AGENT_TASK.md` - Overordnede kvalitetskrav
- `TASK01_analysis.md` - Detaljeret analyse
- `TASK01_implementation.md` - Implementeringsplan

**Test-cases:**
| Input | Forventet resultat |
|-------|-------------------|
| Normal request | 200 OK |
| Malformed request line | 400 Bad Request |
| Invalid UTF-8 bytes | 400 Bad Request |
| Handler exception | 500 Internal Server Error |
| WiFi timeout | System fortsætter på AP |

________________________________________


Engineering Log – 2026-02-04 (fortsat)
Titel: TASK02 Fase 2 - Dependency Injection og fjernelse af global state
________________________________________

Kontekst

Som del af den formaliserede software engineering workflow fortsættes refaktoreringen fra Fase 1. Denne fase fokuserer på at forbedre kodearkitekturen ved at fjerne global state og introducere dependency injection.

________________________________________

Mål for sessionen

• Fjerne global `_heater` variabel fra http_server.py
• Konvertere http_server fra funktioner til klasse med dependency injection
• Gøre afhængigheder eksplicitte og synlige
• Bevare sniffer som global tool (pragmatisk beslutning)

________________________________________

Observationer

**Problem med global state:**

```python
# Før: Skjult afhængighed
_heater = None  # Global variabel

def turn_on(client):
    _heater.turn_on()  # Hvor kommer _heater fra?

# I main.py:
http_server._heater = heater  # Direkte modul-manipulation
```

**Problemer:**
1. Afhængighed er skjult - svært at se hvad funktionen behøver
2. Kan ikke teste isoleret uden at manipulere modul-state
3. Risiko for None-reference hvis _heater ikke er sat
4. Tight coupling mellem main.py og http_server implementation

________________________________________

Hypotese / Analyse

**Dependency Injection princippet:**

> "Don't call us, we'll call you" (Hollywood Principle)

I stedet for at lade http_server selv finde sin afhængighed (global variabel), får den afhængigheden leveret (injiceret) ved konstruktion.

**Fordele ved dependency injection:**

| Aspekt | Global State | Dependency Injection |
|--------|--------------|---------------------|
| Afhængighed synlig? | Nej (skjult i kode) | Ja (i constructor) |
| Testbar? | Svært (kræver modul-hack) | Nemt (inject mock) |
| Fejl ved manglende dep? | Runtime (None error) | Konstruktionstid |
| Kobling | Tight | Loose |

**Pragmatisk beslutning om sniffer:**

Snifferen er et **engangs-udviklingsværktøj**, ikke produktionskode. At refaktorere den ville være over-engineering. Den forbliver som global instance - "good enough" for sit formål.

________________________________________

Beslutning

1. Konverter http_server.py til `HttpServer` klasse
2. Heater injiceres via constructor
3. Alle endpoint-funktioner bliver metoder (med `self`)
4. Private metoder prefixes med underscore (`_turn_on`, `_status`)
5. Sniffer forbliver global (pragmatisk)
6. Opdater main.py til at instantiere HttpServer

________________________________________

Resultat

**http_server.py - Ny klassestruktur:**

```python
class HttpServer:
    """HTTP server with explicit HeaterService dependency."""

    def __init__(self, heater):
        """Initialize with heater service dependency."""
        self.heater = heater  # Eksplicit afhængighed

    def handle_client(self, client):
        """Handle incoming HTTP request."""
        # ... parsing logic ...
        self._route_request(client, path, query)

    def _route_request(self, client, path, query):
        """Route request to appropriate handler."""
        if path == "/":
            self._index(client)
        elif path == "/status":
            self._status(client)
        elif path == "/on":
            self._turn_on(client)
        # ...

    def _turn_on(self, client):
        """Turn heater on."""
        self.heater.turn_on()  # Bruger self.heater, ikke global
        self._send_response(client, 200, "OK", "Heater turned ON")
```

**main.py - Brug af klassen:**

```python
# FØR:
import http_server
http_server._heater = heater  # Modul-manipulation
http_server.handle_client(client)

# EFTER:
from http_server import HttpServer
http = HttpServer(heater)  # Dependency injection
http.handle_client(client)
```

**Komplet ændring i run_server_loop:**

```python
def run_server_loop(heater, mqtt):
    # Create HTTP server with dependency injection
    http = HttpServer(heater)  # <-- Eksplicit afhængighed

    # ... socket setup ...

    while True:
        try:
            client, client_addr = s.accept()
            http.handle_client(client)  # <-- Brug instance
        # ...
```

________________________________________

Konsekvens / Læring

**Tekniske læringer**

1. *Eksplicitte afhængigheder er self-documenting*: Ved at se `HttpServer(heater)` er det klart hvad serveren behøver for at fungere.

2. *Constructor injection er simpelt og effektivt*: Ingen behov for komplekse DI-frameworks i MicroPython - simpel constructor-parameter er tilstrækkeligt.

3. *Underscore-prefix for private metoder*: Python-konvention der signalerer "intern implementation, ikke del af public API".

4. *Pragmatisme over dogmatisme*: Ikke alt skal refaktoreres. Sniffer er et tool, ikke produktionskode - "good enough" er godt nok.

**Arkitektoniske læringer**

1. *Loose coupling enables change*: Hvis HeaterService-interface ændres, skal kun ét sted opdateres (ikke spredt over globale referencer).

2. *Testbarhed som kvalitetsmål*: Kode der er svær at teste er ofte et tegn på dårlig arkitektur.

**Software Engineering principper demonstreret**

- Dependency Injection (DI)
- Inversion of Control (IoC)
- Single Responsibility (klassen har ét ansvar)
- Encapsulation (private metoder med underscore)
- Pragmatic Programming (sniffer undtages)

________________________________________

Kode / Output / Referencer

**Ændrede filer:**
- `http_server.py` - Konverteret til klasse med DI
- `main.py` - Bruger HttpServer klasse

**Workflow dokumenter:**
- `TASK02_implementation.md` - Implementeringsplan for Fase 2

**Ny klassestruktur:**
```
HttpServer
├── __init__(heater)      # Dependency injection
├── handle_client(client) # Public entry point
├── _route_request()      # Private routing
├── _send_response()      # Private helper
├── _status()             # Heater endpoint
├── _turn_on()            # Heater endpoint
├── _turn_off()           # Heater endpoint
├── _sniffer_page()       # Tool endpoint
└── ...
```

**Test:**
Systemet fungerer som før, men med renere arkitektur.

________________________________________


Engineering Log – 2026-02-15
Titel: WiFi-konfiguration på båden og første UART sniffer-test med fysisk varmer
________________________________________

Kontekst

Første test af systemet i det faktiske driftsmiljø - på båden med adgang til det lokale WiFi-netværk og den fysiske dieselvarmer med fjernbetjening.

________________________________________

Mål for sessionen

• Konfigurere ESP32 til at forbinde til bådens WiFi-netværk
• Verificere HTTP-interface fungerer over bådens netværk
• Teste UART sniffer med den faktiske fjernbetjening
• Identificere kommunikationsprotokol mellem remote og varmer

________________________________________

Setup / Forudsætninger

• ESP32 med MicroPython og alle moduler uploadet
• Bådens WiFi-netværk: "The Boat" (WPA2-Personal)
• Dieselvarmer med original fjernbetjening
• PC med Thonny IDE tilsluttet ESP32 via USB

________________________________________

Observationer

**1. WiFi-konfiguration**

Opdaterede `config.py` med bådens WiFi-credentials:
```python
WIFI_SSID = "The Boat"
WIFI_PASSWORD = "31080015"
```

**2. WiFi "Internal State Error"**

Ved første forsøg på at forbinde opstod fejl:
```
WiFi: Connecting to 'The Boat'...
WiFi: Connection error - Wifi Internal State Error
```

Manuel test i REPL virkede:
```python
>>> sta.connect("The Boat", "31080015")
>>> sta.isconnected()
True
```

**Årsag:** WiFi-modulet skal nulstilles før forbindelse.

**Løsning:** Opdaterede `wifi_sta.py` med reset-sekvens:
```python
sta.active(False)
time.sleep(0.5)
sta.active(True)
```

**3. Succesfuld WiFi-forbindelse**

Efter rettelse:
```
[2/4] Connecting to WiFi...
WiFi: Connecting to 'The Boat'...
...
WiFi: Connected!
WiFi: IP address: 192.168.0.148
```

HTTP-interface tilgængelig på http://192.168.0.148/

**4. UART Sniffer stabilitetsproblemer**

Ved test af sniffer med fjernbetjening:
- Første 2-3 captures fungerede
- Derefter timeout ved yderligere captures
- Baud rate-skift loadede ikke

**Diagnose:** Hukommelsesproblemer og manglende UART-cleanup.

**Løsning:** Opdaterede `uart_sniffer.py`:
- Tilføjede `gc.collect()` efter captures
- Tilføjede `_cleanup_uart()` metode med proper deinit
- Tilføjede error handling omkring UART init

**5. Forkert pin-forbindelse**

Captures viste kun nuller (00 00 00...):
```
HEX: 00 00 00 00 00 00 00 00 00 00...
```

**Årsag:** Ledning var forbundet til remotens RX-pin i stedet for TX-pin.

Ved reverse engineering af seriel kommunikation:
- **TX** = Det remoten **sender** (dette skal vi lytte på)
- **RX** = Det remoten **modtager** (ikke relevant for sniffing)

________________________________________

Problem / Spørgsmål

1. Hvilken baud rate bruger fjernbetjeningen?
2. Hvilken pin på remoten er TX?
3. Er signal-niveau kompatibelt (3.3V vs 5V)?

________________________________________

Hypotese / Analyse

**Mulige årsager til kun nuller:**

| Årsag | Sandsynlighed | Test |
|-------|---------------|------|
| Forkert pin (RX i stedet for TX) | Høj | Bekræftet - var forbundet til RX |
| Forkert baud rate | Høj | Skal teste 2400, 4800, 9600 |
| Signal inverteret | Mellem | Ville vise 0xFF i stedet for 0x00 |
| Signal-niveau mismatch (5V→3.3V) | Lav | ESP32 er 5V-tolerant på input |

**Typiske baud rates for dieselvarmere:**
- Kinesiske varmere: Ofte 2400 eller 4800 baud
- Webasto/Eberspächer: Typisk 9600 baud

________________________________________

Beslutning

• Identificer korrekt TX-pin på fjernbetjening
• Tilføj 2400 baud som option i sniffer (var ikke i original menu)
• Test systematisk alle baud rates: 2400, 4800, 9600
• Ved korrekt baud rate forventes varierende data (ikke kun nuller)

________________________________________

Resultat

**Opnået:**
- ✅ WiFi-forbindelse til bådens netværk (192.168.0.148)
- ✅ HTTP-interface verificeret fungerende
- ✅ Sniffer stabilitetsproblemer løst (gc + cleanup)
- ✅ Identificeret forkert pin-forbindelse

**Mangler stadig:**
- ❌ Korrekt fysisk forbindelse til remotens TX
- ❌ Identificering af korrekt baud rate
- ❌ Capture af faktiske kommandoer

**Kodeændringer:**

1. `config.py` - WiFi credentials opdateret
2. `wifi_sta.py` - Tilføjet WiFi reset før connect
3. `uart_sniffer.py` - Tilføjet gc.collect() og bedre cleanup
4. `http_server.py` - Tilføjet 2400 baud option i sniffer

________________________________________

Konsekvens / Læring

**Hardware-læringer**

1. *TX/RX-forvirring er almindelig*: Ved sniffing skal man forbinde til remotens TX (output), ikke RX (input).

2. *WiFi "Internal State Error"*: ESP32's WiFi-modul kan være i ukendt tilstand efter soft reboot. Eksplicit reset (active(False) → active(True)) løser problemet.

3. *Hukommelse på embedded*: MicroPython på ESP32 har begrænset RAM. Garbage collection (`gc.collect()`) er nødvendig efter hukommelsesintensive operationer.

**Proces-læringer**

1. *Test i rigtigt miljø*: Problemer der ikke ses i udvikling (WiFi state, hukommelse) dukker op i produktion.

2. *Systematisk debugging*: Ved at eliminere én variabel ad gangen (først WiFi, så sniffer, så forbindelse) blev problemerne isoleret.

________________________________________

Kode / Output / Referencer

**WiFi-forbindelse:**
```
ESP32 Heater Controller
[1/4] Initializing heater service...
[2/4] Connecting to WiFi...
WiFi: Connecting to 'The Boat'...
WiFi: Connected!
WiFi: IP address: 192.168.0.148
[3/4] Starting AP fallback...
AP: Started 'ESP32-Heater'
[4/4] Skipping MQTT (no WiFi credentials configured)
System ready!
Local HTTP: http://192.168.4.1/
WiFi HTTP:  http://192.168.0.148/
```

**Sniffer hardware-forbindelse (korrekt):**
```
Fjernbetjening          ESP32
┌─────────────┐       ┌─────────┐
│         TX ─┼───────┼── GPIO16│ (RX)
│        GND ─┼───────┼── GND   │
└─────────────┘       └─────────┘
```

**Næste skridt:**
1. Identificer TX-pin på fjernbetjening
2. Lav korrekt forbindelse
3. Test baud rates: 2400, 4800, 9600
4. Capture ON/OFF kommandoer

________________________________________
Engineering Log – 2026-02-16

Titel: UART Sniffer debugging og WebREPL setup

Kontekst
Arbejde på båden med fysisk varmer kørende. ESP32 forbundet via USB (COM3) til laptop. Formål: sniffe UART-kommunikation fra fjernbetjeningen.

Mål for sessionen
• Identificere hvorfor sniffer kun returnerer 00-bytes
• Etablere WiFi-baseret adgang til ESP32 (WebREPL) som alternativ til USB
• Capture faktiske kommandoer fra fjernbetjening

Setup / Forudsætninger
• ESP32: SparkFun IoT RedBoard ESP32, MicroPython v1.27.0
• Forbindelse: USB via COM3 (Silicon Labs CP210x)
• WiFi: Forbundet til "The Boat" (192.168.0.148)
• Varmer: Kørende, fjernbetjening aktiv
• Sniffer pins: GPIO16 (RX), GPIO17 (TX)

Observationer

1. **Signal-detektor udviklet og kørt**
   - Skrev auto-detect script der monitor GPIO16 for transitions
   - Scanner alle baud rates: 1200, 2400, 4800, 9600, 19200, 25000, 38400
   - Resultat: 0 transitions, ingen data ved nogen baud rate

2. **GPIO16 fungerer korrekt**
   - Pin kan drives som output og læses som input
   - Pull-up virker (læser 1 med PULL_UP)
   - Idle state er 1 (HIGH) - korrekt for UART idle
   - UART2 initialiserer uden fejl

3. **Ledning var faldet ud**
   - Første runde af tests: ingen forbindelse overhovedet
   - Ledning blev loddet fast for stabil kontakt
   - Stadig ingen signal efter lodning

4. **GND-forbindelse forstyrrer remoten**
   - Med kun GND forbundet: varmer kører normalt
   - Med COM forbundet til GPIO17 (TX!): varmer slukker
   - Remoteens LCD viser "- - -" (ingen kontakt)

5. **Kritisk fejl fundet: COM var forbundet til GPIO17 (TX) i stedet for GPIO16 (RX)**
   - GPIO17 er ESP32's TX-output → driver aktivt linjen
   - Dette forstyrrede kommunikationen mellem remote og controller
   - Forklarer hvorfor fyret slukkede ved tilslutning
   - GPIO16 (RX) er high-impedance input og burde ikke forstyrre

6. **WebREPL sat op og verificeret**
   - `webrepl_cfg.py` oprettet med password "heater"
   - `boot.py` opdateret til at starte WebREPL automatisk
   - WebSocket-forbindelse verificeret på port 8266
   - `webrepl_cmd.py` wrapper-script skrevet (men har indenteringsproblemer i paste mode)
   - mpremote via WiFi (ws:) virker ikke pålideligt - USB er stadigvæk bedre for kommandoer

Problem / Spørgsmål

1. Selvom COM nu er flyttet til GPIO16 (RX), rapporterer remoten stadig problemer
2. Uklart om remoten ikke kan lide at der lyttes passivt på linjen, eller om der er andet galt
3. Er signalniveau kompatibelt? (remoten kører på 4.8V)
4. Er COM-linjen unidirektionel eller bidirektionel?

Hypotese / Analyse

**Mulige årsager til at remoten forstyrres:**

| Årsag | Sandsynlighed | Forklaring |
|-------|---------------|------------|
| GPIO16 intern pull-up ændrer linje-impedans | Mellem | ESP32 pull-up (45kΩ) kan påvirke svagt signal |
| Forkert pin (stadig TX) | Lav | Blev verificeret, men bør dobbelttjekkes |
| Spændingsmismatch (4.8V vs 3.3V) | Mellem | ESP32 GPIO er 3.3V, input tolerance op til ~3.6V. 4.8V kan være for meget |
| Bidirektionel COM-linje | Høj | Hvis COM bruges til tovejs-kommunikation, kan selv passiv belastning forstyrre |

**Anbefalet løsning: Optocoupler**
En optocoupler (fx PC817 eller 6N137) ville:
- Give galvanisk isolation (ingen fælles GND nødvendig)
- Eliminere enhver elektrisk påvirkning af remotens kommunikation
- Beskytte ESP32 mod overspænding (4.8V → 3.3V)

Beslutning

• Stop hardware-eksperimenter - varmen er kritisk og skal ikke risikeres
• Dokumenter findings og sæt GitHub op
• Ved næste besøg: medbring optocoupler og test med galvanisk isolation

Resultat

**Opnået:**
- ✅ Auto-detect signal script (kører fra mpremote)
- ✅ Bekræftet at GPIO16/17 fungerer korrekt
- ✅ Identificeret TX/RX forveksling som primær fejlkilde
- ✅ WebREPL konfigureret og kørende (port 8266, password "heater")
- ✅ webrepl_cmd.py wrapper-script til WiFi-baserede kommandoer

**Mangler stadig:**
- ❌ Succesfuld UART capture fra remote
- ❌ Afklaring af hvorfor remote forstyrres ved passiv lytning
- ❌ Galvanisk isolation (optocoupler)

**Nye filer:**
1. `webrepl_cfg.py` (på ESP32) - WebREPL password config
2. `boot.py` (opdateret på ESP32) - WebREPL autostart
3. `webrepl_cmd.py` (lokal) - Python wrapper til WiFi-kommandoer

Konsekvens / Læring

1. **TX/RX forveksling er farlig**: At forbinde ESP32's TX til en aktiv kommunikationslinje kan forstyrre eller ødelægge kommunikation. Altid dobbelttjek pin-retning.
2. **Passiv sniffing kræver high-impedance**: Selv en GPIO input pin kan forstyrre følsomme linjer. Optocoupler er den sikre løsning.
3. **Spændingskompatibilitet**: 4.8V på en 3.3V GPIO input er potentielt skadeligt for ESP32 og bør adresseres.
4. **WebREPL fungerer**: Giver mulighed for trådløs adgang, men mpremote over USB er mere pålideligt til interaktiv brug.
5. **Kritisk infrastruktur**: Når man er afhængig af hardware der debugges, skal man have en klar grænse for hvornår man stopper eksperimenter.

Kode / Output / Referencer

**Signal-detektor output (typisk):**
```
=== UART Signal Detector (10 sek) ===
Tryk paa remoten NU!

GPIO16 transitions: 0
GPIO16 final state: 1
>>> INTET SIGNAL paa GPIO16

Baud rate scan (3 sek hver)...
   2400 baud: ingen data
   4800 baud: ingen data
   9600 baud: ingen data
  19200 baud: ingen data
```

**WebREPL test output:**
```
Welcome: 'Password: '
Auth: '\r\nWebREPL connected\r\n>>> '
```

**Indkøbsliste til næste session:**
- Optocoupler (PC817 eller 6N137)
- 330Ω resistor (til optocoupler LED-side)
- 10kΩ resistor (pull-up på optocoupler output-side)

**Optocoupler kredsløb:**
```
Remote COM ──[330Ω]──→ Optocoupler LED+
Remote GND ───────────→ Optocoupler LED-

ESP32 3.3V ──[10kΩ]──→ Optocoupler Collector ──→ GPIO16
ESP32 GND ────────────→ Optocoupler Emitter
```

________________________________________
Engineering Log – 2026-02-18

Titel: Kritiker-agent og sikkerhedsrettelser baseret på kritisk review

Kontekst
Hjemmearbejde efter fysisk session på båden. Projektet var i proof-of-concept-stadie med flere kendte mangler. Formålet var at hæve kodekvaliteten fra prototype til noget der kan bygges videre på.

Mål for sessionen
• Bygge en "kritiker-agent" der systematisk finder problemer i projektet
• Rette de åbenlyse software-mangler identificeret af kritikeren
• Sætte GitHub op og committe alt

Setup / Forudsætninger
• Lokal kode på laptop (ikke på ESP32 - ingen hardware tilsluttet)
• Claude Code som udviklings-AI
• GitHub repo: https://github.com/5uperSune/remote-diesel-heater-control

Observationer

**1. Kritiker-agent udviklet**

Byggede en prototype af en "djævlens advokat" agent bestående af:
- `critic.md` - Prompt-definition med fire reviewer-roller (hardware-skeptiker, sikkerhedsreviewer, arkitektur-kritiker, pålidelighedsingeniør)
- `run_critic.py` - Script der samler al projektkode og genererer input til review

Kritikeren fandt 28 issues: 7 kritiske, 13 advarsler, 8 bemærkninger.

**2. Rettelser implementeret**

| # | Fix | Fil | Alvorlighed |
|---|-----|-----|-------------|
| 1 | TX pin fjernet fra sniffer (`tx=-1`) | `uart_sniffer.py` | KRITISK |
| 2 | Memory cap på captures (max 20) | `uart_sniffer.py` | ADVARSEL |
| 3 | XSS-escaping på sniffer labels | `http_server.py` | ADVARSEL |
| 4 | Ordentlig URL-decoding (%XX sekvenser) | `http_server.py` | BEMÆRKNING |
| 5 | Content-Length beregnet på bytes, ikke tegn | `http_server.py` | BEMÆRKNING |
| 6 | HTTP Basic Auth tilføjet | `http_server.py` | KRITISK |
| 7 | WiFi auto-reconnect (hvert ~60s) | `main.py` | ADVARSEL |
| 8 | Watchdog timer (60s timeout) | `main.py` | ADVARSEL |
| 9 | MQTT heartbeat (hvert ~120s) | `main.py` | ADVARSEL |
| 10 | MQTT last will ("offline" ved disconnect) | `mqtt_client.py` | ADVARSEL |
| 11 | Rate limiting på heater toggle (min 10s) | `heater_service.py` | ADVARSEL |

**3. Bevidst IKKE rettet (kræver hardware eller design-beslutninger)**

- 4.8V spændingsbeskyttelse → kræver optocoupler (hardware)
- MQTT certifikatverifikation → kræver cert deployment
- WebREPL svagt password → skal ændres manuelt på enhed
- HeaterService er stub → venter på UART-protokol

Problem / Spørgsmål

1. `tx=-1` i MicroPython UART - er dette supported på alle ESP32 builds? Skal verificeres ved næste deployment.
2. HTTP Basic Auth sender credentials i klartekst (base64) over HTTP (ikke HTTPS). Acceptabelt for lokalt netværk, men ikke sikkert over internet.
3. Watchdog på 60 sekunder: Er det for kort hvis en UART capture tager 5 sekunder + HTTP response tid?

Hypotese / Analyse

**Kritiker-agent konceptet:**
Idéen om en dedikeret AI-agent der KUN finder problemer (aldrig løsninger) viste sig effektiv. Den fandt issues som:
- TX-pin der aktivt drev COM-linjen (forklarer hardware-problemer på båden)
- XSS-sårbarhed via sniffer labels
- Manglende WiFi reconnect (ville have givet problemer i drift)

Konceptet med at separere "builder" og "critic" rollerne tvinger en mere ærlig evaluering.

**Rate limiting design:**
10 sekunders minimum mellem on/off toggles er konservativt men sikkert for en dieselvarmer. Hurtig toggling kan skade brænder, glødestift og pumpe.

Beslutning

• Alle software-rettelser implementeres nu
• Hardware-rettelser (optocoupler) venter til næste fysiske session
• Kritiker-agent gemmes som værktøj til fremtidige reviews
• GitHub opdateres med alt

Resultat

**Opnået:**
- ✅ Kritiker-agent prototype (`critic.md`, `run_critic.py`)
- ✅ 11 rettelser implementeret (2 kritiske, 7 advarsler, 2 bemærkninger)
- ✅ Alle filer parser korrekt (syntax-verificeret)
- ✅ GitHub repository sat op og synkroniseret

**Kodeændringer:**
1. `uart_sniffer.py` - TX pin fjernet, memory cap tilføjet
2. `http_server.py` - Auth, XSS-escaping, URL-decoding, Content-Length fix
3. `main.py` - Watchdog, WiFi reconnect, MQTT heartbeat
4. `heater_service.py` - Rate limiting med 10s interval
5. `mqtt_client.py` - Last will message
6. `config_example.py` - HTTP auth credentials tilføjet

**Nye filer:**
7. `critic.md` - Kritiker-agent prompt-definition
8. `run_critic.py` - Script til at generere kritisk review

Konsekvens / Læring

1. **Separat kritiker-rolle er værdifuld**: At have en dedikeret "find kun problemer"-agent afdækker blinde punkter som builder-rollen overser.
2. **TX-pin problemet var nøglen**: Kritikeren identificerede at GPIO17 (TX) stadig blev allokeret i snifferen. Dette kan have bidraget til hardware-problemerne på båden, da UART TX aktivt driver linjen.
3. **Prototype ≠ produktionskode**: Selvom projektet er en prototype, skal sikkerhedsfundamentet (auth, XSS, rate limiting) være på plads fra starten - det er svært at tilføje retrospektivt.
4. **Watchdog er essentiel for unattended drift**: En ESP32 der hænger på en båd uden mulighed for manuelt reboot er uacceptabel.

Kode / Output / Referencer

**Kritiker-agent output (sammenfatning):**
```
| Prioritet   | Antal |
|-------------|-------|
| KRITISK     | 7     |
| ADVARSEL    | 13    |
| BEMÆRKNING  | 8     |
```

**Næste skridt:**
1. Deploy opdateret kode til ESP32
2. Verificer `tx=-1` virker i MicroPython v1.27.0
3. Tilføj HTTP_USER/HTTP_PASSWORD til config.py på ESP32
4. Test watchdog under normal drift
5. Medbring optocoupler til næste fysisk session
