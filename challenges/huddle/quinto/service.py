import random
import requests
import time
from datetime import datetime


LOG_SERVER = "http://127.0.0.1:5000/logs"#server url

TOKEN = "http://127.0.0.1:5000/token"#token url

#ask and save token
responese = requests.post(TOKEN)
token = responese.json()["token"]


#list for random logs
services = ["API", "update", "authenticate", "phone-service"]

# Generan logs falsos (pero convincentes).
logs = [
    ("DEBUG", "Variable set to NULL"),
    ("INFO", "Application started successfully"),
    ("WARNING", "Low disk space detected"),
    ("ERROR", "Failed to connect to database"),
    ("CRITICAL", "System shutdown initiated")
]

header = {#Incluyen en el header un token válido con el formato: Authorization: Token TU_TOKEN_AQUÍ
    "Authorization" :"token " + token
}

for _ in range(5):
    severity, msg = random.choice(logs)

    actual_log ={
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": random.choice(services),
        "severity": severity,
        "message" : msg
    }

    #sends the logs with the token
    # Envían estos logs en formato JSON a tu servidor central con método POST.
    response = requests.post(LOG_SERVER,json=actual_log,headers=header)
    print(f"stauts {response.status_code}")  
    time.sleep(1)



# print(actual_log)


