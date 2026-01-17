import os
import requests
from dotenv import load_dotenv

load_dotenv()

def post_results_to_appian(data):
    url = os.getenv("API_POST_URL")
    api_key = os.getenv("API_KEY")

    if not url:
        raise ValueError("API_POST_URL no está definida")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()
