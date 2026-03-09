import time
import re
import requests
from bs4 import BeautifulSoup

def fetch_gift_nifty(max_retries=3):
    for attempt in range(1, max_retries + 1):
        print(f"[Attempt {attempt}/{max_retries}] Fetching GIFT Nifty...")

        price = _fetch_from_investing()
        if price:
            print(f"  -> GIFT Nifty: {price:,.2f}")
            return price

        price = _fetch_from_google()
        if price:
            print(f"  -> GIFT Nifty: {price:,.2f}")
            return price

        if attempt < max_retries:
            print("  -> Failed. Retrying in 5s...")
            time.sleep(5)

    print("  -> All attempts failed.")
    return None

def _fetch_from_investing():
    try:
        url = "https://www.investing.com/indices/sgx-nifty-futures"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for tag, attrs in [
            ("span", {"data-test": "instrument-price-last"}),
            ("span", {"class": "text-5xl"}),
        ]:
            element = soup.find(tag, attrs)
            if element:
                return float(element.text.strip().replace(",", ""))
    except Exception as e:
        print(f"  [Investing.com] Error: {e}")
    return None

def _fetch_from_google():
    try:
        url = "https://www.google.com/search?q=gift+nifty+live+price"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        matches = re.findall(r'(2[2-7],?\d{3}\.?\d{0,2})', text)
        if matches:
            price = float(matches[0].replace(",", ""))
            if 20000 < price < 30000:
                return price
    except Exception as e:
        print(f"  [Google] Error: {e}")
    return None
