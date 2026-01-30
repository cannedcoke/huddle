import mysql.connector
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

#coonect to localhost
conn = mysql.connector.connect(
    host= "localhost",
    user = "root",
    password = ""
)

cursor = conn.cursor()
# create databse and tables
cursor.execute("CREATE DATABASE IF NOT EXISTS logdb")
cursor.execute("USE logdb")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        service VARCHAR(100),
        severity VARCHAR(50),
        message VARCHAR(100)
        
    
    )""")
conn.commit()
conn.close()

def save(log):
    conn = mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = ""
    )

    cursor = conn.cursor()

    cursor.execute("USE logdb")
    cursor.execute("""
                INSERT INTO logs (timestamp, service, severity, message) VALUES (%s,%s,%s,%s)
                """,(log["timestamp"],log["service"],log["severity"],log["message"]))
    conn.commit()
    conn.close()


VALID = ["Whatever"]

# Token
@app.route("/token", methods=["POST"])
def token():
    return jsonify({"token": "Whatever"}),201




# Recibe los logs enviados a: POST /logs
@app.route("/logs",methods=["POST"])
def receive():
    
    token = request.headers.get("Authorization")
    #  Verifica el token de autenticación.
    if not token or token.split()[-1] not in VALID:
        return jsonify({"error ": "invalid token"}),401
    
    data = request.get_json()
    if not data:
        return jsonify({"error":"missing log data"}),400
    
    
    # Guarda los logs en una base de datos.
    save(data)
    return jsonify({"status":"log saved"}),200
    
    
    
    
    
# Endpoint GET /logs con filtros funcionales
@app.route("/logs", methods=["GET"])
def get_logs():
    ts_start = request.args.get("timestamp_start")
    ra_end = request.args.get("received_at_end")
    severity = request.args.get("severity")

    query = "SELECT * FROM logs WHERE 1=1"  #  1 1 lets me nit care about the first condition 

    if ts_start:
        query += f" AND timestamp >= '{ts_start}'"

        query += f" AND received_at <= '{ra_end}'"
    if severity:
        query +=  f" AND severity = '{severity}'"

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("USE logdb")
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    # fromat the output
    output = "ID | Timestamp           | Received At         | Service         | Severity  | Message\n"
    output += "-"*90 + "\n"
    for log in rows:
        output += f"{log['id']:2} | {log['timestamp']} | {log['received_at']} | {log['service']:<15} | {log['severity']:<9} | {log['message']}\n"

    return Response(output, mimetype='text/plain')


if __name__ == "__main__":
    app.run(debug=True)#run on local machine



# http://127.0.0.1:5000/logs?timestamp_start=2026-01-26%2015:20:55&received_at_end=2026-01-26%2016:20:56

# /logs?severity=warning
