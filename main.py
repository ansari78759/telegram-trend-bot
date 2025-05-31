from flask import Flask, request
import telegram
import os
import schedule
import threading
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

CHAT_ID = os.environ.get("CHAT_ID")

app = Flask(__name__)

def send_7pm_message():
    message = "📢 आज का अपडेट:\n🕖 9PM Best Time\n🎵 Trending Audio: 'Chaleya'\n📈 Hashtag: #Reels #Viral"
    bot.send_message(chat_id=CHAT_ID, text=message)

schedule.every().day.at("19:00").do(send_7pm_message)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=run_schedule).start()

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message.text == "/trend":
        bot.send_message(chat_id=update.message.chat.id, text="🎯 आज का ट्रेंड:\n🎵 'Not Ramaiya Vastavaiya'\n📊 #Betting #GrowFast")
    return "ok"

@app.route("/")
def home():
    return "Bot Running OK!"if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
