import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("API_URL")
api_key = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

for item in response.json():
    print(item["nombre"], item["precio"])