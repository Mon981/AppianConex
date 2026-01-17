import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_api():
    url = os.getenv("API_GET_URL")
    api_key = os.getenv("API_KEY")

    if not url:
        raise ValueError("API_URL no está definida en el archivo .env")
    if not api_key:
        raise ValueError("API_KEY no está definida en el archivo .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def get_product_map():
    try:
        products = get_api()
        return [
            {   
                "id": product.get("id"),
                "nombre": product.get("nombre"),
                "precio": product.get("precio")
            }
            for product in products
        ]
    except requests.RequestException as e:
        print(f"Error al consumir la API: {e}")
        return []
    except ValueError as e:
        print(f"Error de configuración: {e}")
        return []

if __name__ == "__main__":
    print(get_product_map())

