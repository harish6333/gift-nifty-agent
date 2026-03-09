import os
import sys
import json
from datetime import datetime, timezone, timedelta

from agent.fetcher import fetch_gift_nifty
from agent.analyzer import generate_message
from agent.notify import send_telegram

IST = timezone(timedelta(hours=5, minutes=30))

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    print("[Config] Loaded successfully.")
    print(f"  Active GTTs: {sum(1 for g in config['gtts'] if g['status'] == 'active')}")
    return config

def should_run(now_ist):
    weekday = now_ist.weekday()
    hour = now_ist.hour
    minute = now_ist.minute
    current_minutes = hour * 60 + minute
    market_open = 9 * 60 + 15
    market_close = 15 * 60 + 30

    if weekday == 5:
        print("[Schedule] Saturday. Skipping.")
        return False
    if weekday == 6:
        if hour < 18:
            print("[Schedule] Sunday before 6 PM. Skipping.")
            return False
        return True
    if market_open <= current_minutes <= market_close:
        print(f"[Schedule] Market is OPEN ({hour}:{minute:02d} IST). Skipping.")
        return False
    print(f"[Schedule] Off-market hours ({hour}:{minute:02d} IST). Running.")
    return True

def main():
    print("=" * 50)
    print("  GIFT NIFTY MONITOR AGENT")
    print("=" * 50)

    test_mode = "--test" in sys.argv
    if test_mode:
        print("[Mode] TEST MODE")

    now_ist = datetime.now(IST)
    print(f"[Time] {now_ist.strftime('%A, %d-%b-%Y %I:%M %p IST')}")

    if not test_mode and not should_run(now_ist):
        return

    config = load_config()

    active_gtts = [g for g in config["gtts"] if g["status"] == "active"]
    if not active_gtts:
        print("[GTTs] No active GTTs. Update config.json.")
        return

    gift_nifty = fetch_gift_nifty()
    if not gift_nifty:
        print("[Result] Could not fetch GIFT Nifty. Will retry next run.")
        return

    message = generate_message(gift_nifty, config)
    print("[Message Preview]")
    print(message)

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if bot_token and chat_id:
        send_telegram(bot_token, chat_id, message)
    else:
        print("[Telegram] Credentials not found. Set GitHub Secrets.")

    print("[Result] Done!")

if __name__ == "__main__":
    main()
