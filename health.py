"""
Minimal health-check web server.

Render's free tier expects the service to respond to HTTP requests on the
port Render provides via the PORT environment variable. This file starts a
tiny web server in a background thread so Render (and UptimeRobot) sees the
service as "alive," while the actual Telegram bot logic keeps running
normally in the main thread.

This file does not replace anything in bot/ — it just adds the missing
piece Render needs.
"""

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running.")

    # Silence default request logging so it doesn't spam the bot's own logs
    def log_message(self, format, *args):
        pass


def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


def start_health_server_in_background():
    thread = threading.Thread(target=run_health_server, daemon=True)
    thread.start()
 
