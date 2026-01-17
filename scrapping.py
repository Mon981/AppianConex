import time
import sys
import os
from contextlib import contextmanager
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


load_dotenv()

@contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

def create_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1200,900")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        }
    )
    return driver, wait

cookies_accepted = False

def accept_cookies(driver, wait):
    global cookies_accepted
    if cookies_accepted:
        return
    try:
        btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Permitir todas') or contains(text(),'Aceptar')]")
            )
        )
        btn.click()
        time.sleep(2)
        cookies_accepted = True
    except:
        pass


def close_modal(driver, wait):
    try:
        btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.cn_content_close-adf93cbc-6fdd-46b7-9fe6-32ed75f57ade a")
            )
        )
        btn.click()
        time.sleep(1)
    except:
        pass

def search_product_price(driver, wait, product_name):
    try:
        seek = wait.until(EC.element_to_be_clickable((By.ID, "seek")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seek)
        driver.execute_script("arguments[0].click();", seek)

        box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.dfd-searchbox-input"))
        )
        box.clear()
        box.send_keys(product_name)
        box.send_keys(Keys.ENTER)

        time.sleep(3)

        products = driver.find_elements(By.CSS_SELECTOR, ".dfd-card")[:3]

        for prod in products:
            try:
                precio_text = prod.find_element(By.CSS_SELECTOR, ".dfd-card-price").text
                precio_text = (
                    precio_text.replace("€", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                return float(precio_text)
            except:
                continue
    except:
        pass

    return None

def scrape_prices(products, on_ready=None):
    driver, wait = create_driver()

    try:
        driver.get(os.getenv("URL_TO_SCRAPPE"))
        time.sleep(2)

        accept_cookies(driver, wait)
        close_modal(driver, wait)

  
        if on_ready:
            on_ready()

        results = []

        for p in products:
            nuevo_precio = search_product_price(driver, wait, p["nombre"])
            results.append({
                "id": p["id"],
                "nombre": p["nombre"],
                "precio_original": p["precio"],
                "precio_nuevo": nuevo_precio
            })
            time.sleep(2)

        return results

    finally:
        with suppress_stderr():
            try:
                driver.quit()
            except:
                pass