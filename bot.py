
import os
import time
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=20
    )

def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    offset = 0
    print("Gold Telegram bot is running.")

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 25},
                timeout=35
            )
            response.raise_for_status()

            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "").strip()

                if not chat_id:
                    continue

                if text == "/start":
                    send_message(
                        chat_id,
                        "مرحباً بك في بوت الذهب XAUUSD!\n"
                        "البوت قيد التجهيز.\n"
                        "استخدم /status لمعرفة حالة الإعداد."
                    )
                elif text == "/status":
                    send_message(
                        chat_id,
                        "البوت يعمل، لكن تحليل السوق "
                        "وإشارات التداول لم تُفعّل بعد."
                    )

        except Exception as error:
            print(f"Connection error: {error}")
            time.sleep(5)

if __name__ == "__main__":
    main()
