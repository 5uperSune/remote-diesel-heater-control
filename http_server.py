# http_server.py
"""
HTTP server for local heater control and UART sniffer interface.

Uses dependency injection for HeaterService (clean architecture).
Sniffer remains as global tool (development utility, not production code).

Provides endpoints for:
- Heater control: /status, /on, /off
- UART sniffer: /sniffer, /sniffer/capture, /sniffer/data, /sniffer/clear
"""

from uart_sniffer import sniffer  # Development tool, kept as global
import ubinascii

try:
    from config import HTTP_USER, HTTP_PASSWORD
except ImportError:
    HTTP_USER = None
    HTTP_PASSWORD = None


def _html_escape(s):
    """Escape HTML special characters to prevent XSS."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#x27;"))


def _url_decode(s):
    """Decode URL-encoded string (handles %XX sequences and +)."""
    s = s.replace("+", " ")
    parts = s.split("%")
    result = parts[0]
    for part in parts[1:]:
        if len(part) >= 2:
            try:
                result += chr(int(part[:2], 16)) + part[2:]
            except ValueError:
                result += "%" + part
        else:
            result += "%" + part
    return result


class HttpServer:
    """
    HTTP server with explicit HeaterService dependency.

    Usage:
        server = HttpServer(heater_service)
        server.handle_client(client_socket)
    """

    def __init__(self, heater):
        """Initialize with heater service dependency."""
        self.heater = heater
        if HTTP_USER and HTTP_PASSWORD:
            self._auth_token = ubinascii.b2a_base64(
                "{}:{}".format(HTTP_USER, HTTP_PASSWORD).encode()
            ).decode().strip()
        else:
            self._auth_token = None

    def handle_client(self, client):
        """Handle incoming HTTP request."""
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
                self._send_response(client, 400, "Bad Request", "Invalid encoding")
                return

            # 3. Parse request line safely
            lines = request.split("\r\n")
            if not lines or not lines[0]:
                print("HTTP: Empty request")
                self._send_response(client, 400, "Bad Request", "Empty request")
                return

            parts = lines[0].split()
            if len(parts) < 2:
                print("HTTP: Malformed request line")
                self._send_response(client, 400, "Bad Request", "Malformed request")
                return

            method = parts[0]
            path = parts[1]

            # 4. Check authentication
            if self._auth_token:
                auth_ok = False
                for line in lines[1:]:
                    if line.lower().startswith("authorization: basic "):
                        token = line.split(" ", 2)[2].strip()
                        if token == self._auth_token:
                            auth_ok = True
                        break
                if not auth_ok:
                    client.send(
                        "HTTP/1.1 401 Unauthorized\r\n"
                        "WWW-Authenticate: Basic realm=\"Heater\"\r\n"
                        "Content-Length: 12\r\n\r\n"
                        "Unauthorized"
                    )
                    return

            # 5. Extract query string if present
            query = ""
            if "?" in path:
                path, query = path.split("?", 1)

            print("HTTP:", method, path)

            # 5. Route request with exception handling
            try:
                self._route_request(client, path, query)
            except Exception as e:
                print("HTTP: Handler error -", e)
                try:
                    self._send_response(client, 500, "Internal Server Error", "Server error")
                except:
                    pass  # Client may have disconnected

        except Exception as e:
            print("HTTP: Request error -", e)

        finally:
            try:
                client.close()
            except:
                pass

    def _route_request(self, client, path, query):
        """Route request to appropriate handler."""
        # Heater endpoints
        if path == "/":
            self._index(client)
        elif path == "/status":
            self._status(client)
        elif path == "/on":
            self._turn_on(client)
        elif path == "/off":
            self._turn_off(client)
        # Sniffer endpoints (tool - uses global sniffer)
        elif path == "/sniffer":
            self._sniffer_page(client)
        elif path == "/sniffer/capture":
            self._sniffer_capture(client, query)
        elif path == "/sniffer/data":
            self._sniffer_data(client)
        elif path == "/sniffer/clear":
            self._sniffer_clear(client)
        elif path == "/sniffer/delete":
            self._sniffer_delete(client, query)
        elif path == "/sniffer/baud":
            self._sniffer_set_baud(client, query)
        else:
            self._not_found(client)

    # ============ Response helpers ============

    def _send_response(self, client, status_code, status_text, body, content_type="text/plain"):
        """Send HTTP response."""
        body_bytes = body.encode("utf-8") if isinstance(body, str) else body
        response = (
            "HTTP/1.1 {} {}\r\n"
            "Content-Type: {}\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(status_code, status_text, content_type, len(body_bytes))
        client.send(response)
        client.send(body_bytes)

    def _send_html(self, client, body):
        """Send HTML response."""
        self._send_response(client, 200, "OK", body, "text/html; charset=utf-8")

    def _redirect(self, client, location):
        """Send redirect response."""
        response = "HTTP/1.1 302 Found\r\nLocation: {}\r\n\r\n".format(location)
        client.send(response)

    # ============ Heater endpoints ============

    def _index(self, client):
        """Show available endpoints."""
        body = "ESP32 Heater Controller\n\nEndpoints:\n  /status\n  /on\n  /off\n  /sniffer"
        self._send_response(client, 200, "OK", body)

    def _status(self, client):
        """Return heater status."""
        body = "Heater status: " + self.heater.status()
        self._send_response(client, 200, "OK", body)

    def _turn_on(self, client):
        """Turn heater on."""
        if self.heater.turn_on():
            self._send_response(client, 200, "OK", "Heater turned ON")
        else:
            self._send_response(client, 429, "Too Many Requests",
                                "Rate limited - wait before toggling again")

    def _turn_off(self, client):
        """Turn heater off."""
        if self.heater.turn_off():
            self._send_response(client, 200, "OK", "Heater turned OFF")
        else:
            self._send_response(client, 429, "Too Many Requests",
                                "Rate limited - wait before toggling again")

    def _not_found(self, client):
        """Return 404."""
        self._send_response(client, 404, "Not Found", "404 Not Found")

    # ============ Sniffer endpoints (development tool) ============

    def _sniffer_page(self, client):
        """Main sniffer page with input form."""
        captures = sniffer.get_all_captures()

        # Build captures table
        captures_html = ""
        if captures:
            for i, cap in enumerate(captures):
                hex_data = sniffer.format_hex(cap["data"]) if cap["data"] else "(ingen data)"
                captures_html += """
                <tr>
                    <td>{}</td>
                    <td><strong>{}</strong></td>
                    <td>{} bytes</td>
                    <td style="font-family:monospace;font-size:12px">{}</td>
                    <td><a href="/sniffer/delete?i={}">Slet</a></td>
                </tr>
                """.format(i + 1, _html_escape(cap["label"]), cap["bytes"], hex_data, i)
        else:
            captures_html = '<tr><td colspan="5">Ingen captures endnu</td></tr>'

        html = """<!DOCTYPE html>
<html>
<head>
    <title>UART Sniffer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        .form-group {{ margin: 20px 0; padding: 20px; background: #e8f4e8; border-radius: 8px; }}
        input[type="text"] {{ width: 100%; padding: 15px; font-size: 18px; border: 2px solid #4CAF50; border-radius: 4px; box-sizing: border-box; }}
        button {{ padding: 15px 30px; font-size: 18px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }}
        button:hover {{ background: #45a049; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
        th {{ background: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .info {{ background: #e7f3fe; padding: 15px; border-radius: 4px; margin: 10px 0; }}
        .actions {{ margin-top: 20px; }}
        .actions a {{ margin-right: 10px; color: #4CAF50; }}
        .baud {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>UART Sniffer</h1>

        <div class="info">
            <strong>Baud rate:</strong> {baud}
            <span class="baud">
                <a href="/sniffer/baud?b=2400">2400</a> |
                <a href="/sniffer/baud?b=4800">4800</a> |
                <a href="/sniffer/baud?b=9600">9600</a> |
                <a href="/sniffer/baud?b=19200">19200</a> |
                <a href="/sniffer/baud?b=25000">25000</a>
            </span>
        </div>

        <div class="form-group">
            <form action="/sniffer/capture" method="get">
                <label for="label"><strong>Hvad vil du capture?</strong></label><br><br>
                <input type="text" id="label" name="label" placeholder="Skriv kommando her, fx Mountain mode" required>
                <br>
                <button type="submit">Capture (5 sek)</button>
            </form>
        </div>

        <h2>Captures ({count})</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Label</th>
                <th>Size</th>
                <th>Data (HEX)</th>
                <th></th>
            </tr>
            {captures}
        </table>

        <div class="actions">
            <a href="/sniffer">Opdater</a>
            <a href="/sniffer/clear" onclick="return confirm('Slet alle captures?')">Ryd alle</a>
            <a href="/">Tilbage til heater</a>
        </div>
    </div>
</body>
</html>""".format(
            baud=sniffer.baud,
            count=len(captures),
            captures=captures_html
        )

        self._send_html(client, html)

    def _sniffer_capture(self, client, query):
        """Capture UART data with given label."""
        # Parse label from query string
        label = "Unknown"
        if query:
            for param in query.split("&"):
                if param.startswith("label="):
                    label = _url_decode(param[6:])
                    break

        # Do the capture (blocks for 5 seconds)
        result = sniffer.capture(label)

        # Show result page
        hex_data = sniffer.format_hex(result["data"]) if result["data"] else "(ingen data)"
        ascii_data = sniffer.format_ascii(result["data"]) if result["data"] else ""

        html = """<!DOCTYPE html>
<html>
<head>
    <title>Capture resultat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .success {{ background: #d4edda; padding: 20px; border-radius: 4px; }}
        .data {{ background: #f8f9fa; padding: 15px; margin: 10px 0; font-family: monospace; border-radius: 4px; word-break: break-all; }}
        a {{ color: #4CAF50; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success">
            <h2>Capture: {label}</h2>
            <p><strong>Bytes:</strong> {bytes}</p>
        </div>

        <h3>HEX</h3>
        <div class="data">{hex}</div>

        <h3>ASCII</h3>
        <div class="data">{ascii}</div>

        <p>
            <a href="/sniffer">Tilbage til sniffer</a>
        </p>
    </div>
</body>
</html>""".format(
            label=_html_escape(label),
            bytes=result["bytes"],
            hex=hex_data,
            ascii=ascii_data
        )

        self._send_html(client, html)

    def _sniffer_data(self, client):
        """Show all captured data as plain text."""
        captures = sniffer.get_all_captures()

        lines = ["UART SNIFFER DATA", "=" * 40, ""]

        for i, cap in enumerate(captures):
            lines.append("#{} - {}".format(i + 1, cap["label"]))
            lines.append("Bytes: {}".format(cap["bytes"]))
            lines.append("HEX: {}".format(sniffer.format_hex(cap["data"])))
            lines.append("ASCII: {}".format(sniffer.format_ascii(cap["data"])))
            lines.append("")

        if not captures:
            lines.append("Ingen captures endnu.")

        self._send_response(client, 200, "OK", "\n".join(lines))

    def _sniffer_clear(self, client):
        """Clear all captures."""
        sniffer.clear_captures()
        self._redirect(client, "/sniffer")

    def _sniffer_delete(self, client, query):
        """Delete a specific capture."""
        index = 0
        if query:
            for param in query.split("&"):
                if param.startswith("i="):
                    try:
                        index = int(param[2:])
                    except:
                        pass
                    break

        sniffer.delete_capture(index)
        self._redirect(client, "/sniffer")

    def _sniffer_set_baud(self, client, query):
        """Set baud rate."""
        baud = 9600
        if query:
            for param in query.split("&"):
                if param.startswith("b="):
                    try:
                        baud = int(param[2:])
                    except:
                        pass
                    break

        sniffer.set_baud(baud)
        self._redirect(client, "/sniffer")
