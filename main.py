from flask import Flask, request
import telegram
import os
import openai
import schedule
import threading
import time

# 📦 Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telegram.Bot(token=BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# 🧠 GPT से Trend Data Generate Function
def get_trend_update():
    prompt = """
Give today's Instagram Reels content idea based on trending topics.
Return the result in this format:
Caption: [a short and creative caption]
Hashtags: [5 trending hashtags]
Trending Audio: [trending song/audio name]
"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "❌ GPT Error: " + str(e)

# 📩 Flask Webhook
@app.route('/')
def home():
    return "✅ Sohail Trend Bot Live!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"].strip().lower()

        if user_msg == "/trend":
            trend_message = get_trend_update()
            bot.send_message(chat_id=chat_id, text=trend_message)

    return "OK"

# 🔁 Daily Auto 7PM Message
def send_daily_update():
    trend_message = get_trend_update()
    bot.send_message(chat_id=CHAT_ID, text=trend_message)

# ⏰ Scheduler Thread
def run_schedule():
    schedule.every().day.at("19:00").do(send_daily_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

# 🚀 Run Flask App
if __name__ == "__main__":
    print("✅ Sohail Trend Bot Running")
    app.run(host="0.0.0.0", port=10000)
