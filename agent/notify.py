import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}/'

    def send_message(self, chat_id, message):
        url = self.base_url + 'sendMessage'
        payload = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=payload)
        return response.json()

# Example usage
if __name__ == '__main__':
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    message = 'Hello, this is a test message!'

    bot = TelegramBot(bot_token)
    result = bot.send_message(chat_id, message)
    print(result)