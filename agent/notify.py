import requests

def send_telegram(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        print("[Telegram] ERROR: Credentials not set.")
        return False
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        if data.get("ok"):
            print("[Telegram] ✅ Message sent!")
            return True
        else:
            print(f"[Telegram] ❌ Failed: {data.get('description')}")
            return False
    except Exception as e:
        print(f"[Telegram] ❌ Error: {e}")
        return False
