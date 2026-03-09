import requests

def analyze_gift_nifty(data, gtt_levels):
    results = []
    for level in gtt_levels:
        if data['nifty'] >= level['target']:
            results.append(f"Nifty has reached the GTT level: {level['target']}!")
            send_telegram_message(f"Nifty has reached the GTT level: {level['target']}!")
    return results


def send_telegram_message(message):
    # Define your Telegram bot token and chat ID here
    bot_token = '8256252960:AAE-VXi7gy3vLKYN8PPycv5h3roj-4mw4vY'
    chat_id = '7277821533'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

# Example use
if __name__ == '__main__':
    gift_nifty_data = {'nifty': 15000}
    gtt_levels = [{'target': 14900}, {'target': 15100}]
    analyze_gift_nifty(gift_nifty_data, gtt_levels)
