from flask import Flask, request
import telegram
import os
import schedule
import threading
import time

# Telegram Bot Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

# Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is Live ✅"

# Telegram Command Handler
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"]

        if user_msg == "/trend":
            message = "📈 आज का ट्रेंड:\n🕖 9PM Best Time\n🎵 Trending Audio: 'Chaleya'\n🏷️ Hashtag: #Reels #Explore #Foryou"
            bot.send_message(chat_id=chat_id, text=message)

    return "OK"

# Auto Daily 7PM Reminder
def send_7pm_message():
    message = "📢 आज का अपडेट:\n🕖 9PM Best Time\n🎵 Trending Audio: 'Chaleya'\n🏷️ Hashtag: #Reels #Explore #Foryou"
    bot.send_message(chat_id=CHAT_ID, text=message)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("19:00").do(send_7pm_message)
threading.Thread(target=run_schedule).start()

# Final Flask run
if __name__ == "__main__":
    print("✅ Bot Running OK!")
    app.run(host="0.0.0.0", port=10000)
