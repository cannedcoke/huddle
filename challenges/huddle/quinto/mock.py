import requests


LOG_SERVER = "http://127.0.0.1:5000/logs"#server url

TOKEN = "http://127.0.0.1:5000/token"#token url


req = requests.post(TOKEN)

token = req.json()["token"]

log = [{"status":"susccesful"}]

header ={
    "Authorization": token
}

requests.post(LOG_SERVER,json=log,headers=header)
