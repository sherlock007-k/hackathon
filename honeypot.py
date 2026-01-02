# ---------------- honeypot.py ----------------
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

LOG_FILE = "attacker_log.txt"

class Honeypot(BaseHTTPRequestHandler):
    def do_GET(self):
        attacker_ip = self.client_address[0]

        # Dummy geo plot for demo — default location points to India
        lat, lon = 28.6139, 77.2090   # New Delhi (safe placeholder)

        with open(LOG_FILE, "a") as f:
            f.write(f"{attacker_ip},{lat},{lon}\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Fake vulnerable device...")

try:
    server = HTTPServer(("0.0.0.0", 8081), Honeypot)
    print("🕵 Honeypot Active on port 8081 — waiting for attacker...")
    server.serve_forever()

except KeyboardInterrupt:
    print("Stopped")
