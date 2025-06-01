import os
import time
import openai
import schedule
import threading
from flask import Flask, request
from telegram import Bot

# Telegram Credentials

BOT_TOKEN = "7883457826:AAGEZ72ipQTpRrECa1Rzpmi_TSvrqgtnB44"
CHAT_ID = "6544146670"
bot = Bot(token=BOT_TOKEN)

# GPT API Key
openai.api_key = "OPENAI_API_KEY"

# Flask App
app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"]

        if user_msg == "/trend":
            message = "📢 आज का अपडेट:\n🎯 9PM Best Time\n🎵 Trending Audio: 'Chaleya'\n🏷️ Hashtag: #Reels #Explore #Foryou"
        else:
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_msg}]
            )
            message = gpt_response.choices[0].message.content

        bot.send_message(chat_id=chat_id, text=message)

    return "OK"

# 7PM Daily Message
def send_7pm_message():
    message = "📢 आज का अपडेट:\n🎯 9PM Best Time\n🎵 Trending Audio: 'Chaleya'\n🏷️ Hashtag: #Reels #Explore #Foryou"
    bot.send_message(chat_id=CHAT_ID, text=message)

# Schedule Background Thread
schedule.every().day.at("19:00").do(send_7pm_message)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

# Flask Run
if __name__ == "__main__":
    print("✅ Bot Running OK!")
    app.run(host="0.0.0.0", port=10000)
