"""
Critic Agent - Den Irriterende Kollega
Samler projektfiler og genererer en kritisk review-rapport.

Brug: Kør dette script, og giv outputtet til Claude Code med prompten fra critic.md
Eller brug det direkte i Claude Code med: /critic
"""

import os
import sys

# Filer der skal reviewes
PROJECT_FILES = [
    "main.py",
    "heater_service.py",
    "http_server.py",
    "mqtt_client.py",
    "uart_sniffer.py",
    "wifi_sta.py",
    "wifi_ap.py",
    "config_example.py",
]

# Filer der IKKE må inkluderes (credentials)
EXCLUDED = ["config.py", "webrepl_cmd.py", "webrepl_cfg.py"]

def collect_project_context(project_dir):
    """Samler al relevant projektkode i ét dokument."""

    output = []
    output.append("=" * 60)
    output.append("PROJEKT TIL KRITISK REVIEW")
    output.append("ESP32 Diesel Heater Control Gateway")
    output.append("=" * 60)
    output.append("")

    # Saml kildekode
    output.append("## KILDEKODE")
    output.append("")

    for filename in PROJECT_FILES:
        filepath = os.path.join(project_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            output.append(f"### {filename}")
            output.append(f"```python")
            output.append(content)
            output.append(f"```")
            output.append("")

    # Saml seneste engineering log entry
    log_path = os.path.join(project_dir, "Engineering_Log.md")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
        # Tag kun sidste 3000 tegn (seneste entries)
        output.append("## SENESTE ENGINEERING LOG (uddrag)")
        output.append("```")
        output.append(log_content[-3000:])
        output.append("```")
        output.append("")

    # Hardware info
    output.append("## HARDWARE SETUP")
    output.append("- Board: SparkFun IoT RedBoard ESP32 (ESP32-WROOM-32)")
    output.append("- MicroPython v1.27.0")
    output.append("- Varmer: Kinesisk dieselvarmer, single-wire COM bus (4.8V)")
    output.append("- UART2: GPIO16 (RX), GPIO17 (TX)")
    output.append("- LEDs: GPIO18 (grøn), GPIO19 (rød)")
    output.append("- WiFi: STA + AP mode")
    output.append("- MQTT: HiveMQ Cloud med TLS")
    output.append("- WebREPL: Port 8266, aktiv")
    output.append("")

    # Tjek for credentials-lækage
    output.append("## CREDENTIALS CHECK")
    for excluded in EXCLUDED:
        path = os.path.join(project_dir, excluded)
        if os.path.exists(path):
            output.append(f"- {excluded} EKSISTERER lokalt (bør IKKE committes)")
    output.append("")

    return "\n".join(output)


def generate_review_prompt(context):
    """Genererer den fulde prompt til kritiker-agenten."""

    prompt = f"""Du er en erfaren, kritisk ingeniør-reviewer. Find ALLE problemer, risici og mangler.

Vær specifik. Vær direkte. Ingen pæne ord.

Prioriter: 🔴 KRITISK > 🟡 ADVARSEL > 🔵 BEMÆRKNING

Kategorier:
1. HARDWARE & ELEKTRICITET
2. SIKKERHED
3. PÅLIDELIGHED & FEJLHÅNDTERING
4. ARKITEKTUR & KODE
5. DRIFT & VEDLIGEHOLD

For hver finding:
- Hvad er problemet (specifikt, med filnavn og linje hvis relevant)
- Hvorfor er det et problem
- Hvor alvorligt er det

Foreslå IKKE løsninger. Kun problemer.

---

{context}

---

GIV DIN KRITISKE REVIEW NU:"""

    return prompt


if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))

    context = collect_project_context(project_dir)
    prompt = generate_review_prompt(context)

    # Output til fil som kan bruges med Claude Code
    output_path = os.path.join(project_dir, "critic_input.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"Critic input genereret: {output_path}")
    print(f"Størrelse: {len(prompt)} tegn")
    print()
    print("Brug i Claude Code:")
    print('  Bed Claude: "Læs critic_input.txt og giv mig din kritiske review"')
    print()

    # Print også til stdout for direkte brug
    if "--print" in sys.argv:
        print(prompt)
