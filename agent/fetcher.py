import requests
import time

class NiftyFetcher:
    def __init__(self, url, retries=3, delay=2):
        self.url = url
        self.retries = retries
        self.delay = delay

    def fetch_live_price(self):
        for attempt in range(self.retries):
            try:
                response = requests.get(self.url)
                response.raise_for_status()  # Raises an error for bad responses
                data = response.json()
                # Assuming the price is in a field called 'price'
                return data['price']
            except (requests.HTTPError, requests.ConnectionError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(self.delay)  # Wait before retrying
        raise Exception('Failed to fetch live price after several retries')

# Example usage:
# fetcher = NiftyFetcher('https://api.example.com/nifty-price')
# price = fetcher.fetch_live_price()
# print(price)