import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import mysql.connector
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

VALID_TOKENS = ["Whatever"]

# ---------- DB SETUP ----------
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS logdb")
    cursor.execute("USE logdb")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            service VARCHAR(100),
            severity VARCHAR(50),
            message VARCHAR(100)
        )
    """)
    conn.commit()
    conn.close()


def save_log(log):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="logdb"
    )
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, service, severity, message)
        VALUES (%s, %s, %s, %s)
    """, (
        log["timestamp"],
        log["service"],
        log["severity"],
        log["message"]
    ))
    conn.commit()
    conn.close()


# ---------- HTTP HANDLER ----------
class LogServer(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_text(self, text, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(text.encode())

    # -------- POST --------
    def do_POST(self):
        parsed = urlparse(self.path)

        # POST /token
        if parsed.path == "/token":
            self._send_json({"token": "Whatever"}, 201)
            return

        # POST /logs
        if parsed.path == "/logs":
            auth = self.headers.get("Authorization")
            if not auth or auth.split()[-1] not in VALID_TOKENS:
                self._send_json({"error": "invalid token"}, 401)
                return

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._send_json({"error": "invalid json"}, 400)
                return

            save_log(data)
            self._send_json({"status": "log saved"}, 200)
            return

        self._send_json({"error": "not found"}, 404)

    # -------- GET --------
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/logs":
            self._send_json({"error": "not found"}, 404)
            return

        params = parse_qs(parsed.query)

        query = "SELECT * FROM logs WHERE 1=1"
        values = []

        if "timestamp_start" in params:
            query += " AND timestamp >= %s"
            values.append(params["timestamp_start"][0])

        if "timestamp_end" in params:
            query += " AND timestamp <= %s"
            values.append(params["timestamp_end"][0])

        if "received_at_start" in params:
            query += " AND received_at >= %s"
            values.append(params["received_at_start"][0])

        if "received_at_end" in params:
            query += " AND received_at <= %s"
            values.append(params["received_at_end"][0])

        if "severity" in params:
            query += " AND severity = %s"
            values.append(params["severity"][0])

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="logdb"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, values)
        rows = cursor.fetchall()
        conn.close()

        output = (
            "ID | Timestamp           | Received At         | Service         | Severity  | Message\n"
            + "-" * 90 + "\n"
        )

        for log in rows:
            output += (
                f"{log['id']:2} | {log['timestamp']} | {log['received_at']} | "
                f"{log['service']:<15} | {log['severity']:<9} | {log['message']}\n"
            )

        self._send_text(output, 200)


# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    server = HTTPServer((HOST, PORT), LogServer)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()
