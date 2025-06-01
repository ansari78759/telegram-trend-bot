from flask import Flask, request
import telegram
import os
import openai
import schedule
import threading
import time

# Load environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telegram.Bot(token=BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# GPT prompt generator
def generate_trend_update(category):
    prompt = f"""
    Give a trending Instagram post idea in the {category} category.
    Include:
    - A highly engaging caption (influencer style)
    - 5 trending hashtags
    - One trending music/audio suggestion
    - Best upload time (in IST) for highest reach (90%+ chance)
    Format:
    📸 Caption:
    🎵 Music:
    ⏰ Time:
    🏷️ Hashtags:
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT Error: {str(e)}"

# Flask Home
@app.route('/')
def home():
    return "✅ Sohail Trend Bot Running"

# Webhook handler
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"].strip().lower()

        if user_msg.startswith("/trend"):
            category = user_msg.replace("/trend", "").strip() or "general"
            reply = generate_trend_update(category)
            bot.send_message(chat_id=chat_id, text=reply)

    return "OK"

# Auto 7PM daily push

def send_daily_update():
    update = generate_trend_update("general")
    bot.send_message(chat_id=CHAT_ID, text=update)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("19:00").do(send_daily_update)
threading.Thread(target=run_schedule).start()

# Run Flask app
if __name__ == "__main__":
    print("✅ Sohail Trend Bot Running")
    app.run(host="0.0.0.0", port=10000)
