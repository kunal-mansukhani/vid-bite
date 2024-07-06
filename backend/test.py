import requests
import json



url = "http://localhost:8000/generate_code"

data = {
    "text": "Draw a two layer neural network",
    "style": "default",
    "use_claude": False
}


response = requests.post(url, json=data)

if response.status_code == 200:
    print(response.json())

