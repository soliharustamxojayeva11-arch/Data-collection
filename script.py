from datetime import datetime
import os
import json
import requests

CITY = "Tashkent"
TOKEN = os.getenv("WAQI_TOKEN")
BUFFER_FILE = "buffer.json"
DATA_FILE = "data.csv"

url = f'https://api.waqi.info/feed/{CITY}/?token={TOKEN}'


try:
    response = requests.get(url).json()
    current_pm25 = response["data"]["iaqi"]["pm25"]["v"]
except Exception as e:
    print(f"Error: {e}")
    exit(1)

if os.path.exists(BUFFER_FILE):
    with open(BUFFER_FILE, "r") as f:
        data = json.load(f)
else:
    data = []

data.append(current_pm25)

if len(data) >= 8:
    pm25 = round(sum(data) / len(data), 2)
    date = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(DATA_FILE):  
        with open(DATA_FILE, "w") as f:
            f.write("date,pm25\n")

    with open(DATA_FILE, "a") as f:
        f.write(f"{date},{pm25}\n")
        
    if os.path.exists(BUFFER_FILE):
        os.remove(BUFFER_FILE)   

    print(f"info for today: {date}: {pm25}")
else:
    with open(BUFFER_FILE, "w") as f:
        json.dump(data, f)
    print(f"Saved. Steps: {len(data)} out of 8")
