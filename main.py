from flask import Flask, request
import telegram
import openai
import os
import schedule
import threading
import time
import random

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telegram.Bot(token=BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Function to get GPT response for caption

def generate_caption(category):
    prompt = f"""
    Give a unique, short, viral Instagram reel caption for the "{category}" niche, targeting Indian youth in 2025.
    Include emojis and a strong hook. Make sure it does NOT repeat previous suggestions.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=random.uniform(0.7, 1),
        max_tokens=100
    )
    return response['choices'][0]['message']['content'].strip()

# Trending Hashtags from GPT

def generate_hashtags(category):
    prompt = f"""
    List 15 trending Instagram hashtags for the "{category}" niche that can boost reach in 2025. Use no more than 3 words per hashtag.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=100
    )
    return response['choices'][0]['message']['content'].strip()

# Trending Audio suggestion

def generate_audio(category):
    prompt = f"""
    Suggest one current trending Instagram Reels music/audio for the "{category}" niche (as of June 2025).
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=60
    )
    return response['choices'][0]['message']['content'].strip()

# Best Upload Time

def best_time(category):
    time_map = {
        "fashion": "9:00 PM",
        "fitness": "7:30 PM",
        "food": "12:30 PM",
        "cricket": "1:30 PM",
        "travel": "8:00 PM",
        "default": "6:00 PM"
    }
    return time_map.get(category.lower(), time_map["default"])

@app.route('/')
def home():
    return "✅ Sohail Trend Bot Running"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"].strip().lower()

        if user_msg.startswith("/trend"):
            parts = user_msg.split(" ")
            category = parts[1] if len(parts) > 1 else "general"
            
            caption = generate_caption(category)
            hashtags = generate_hashtags(category)
            audio = generate_audio(category)
            time_to_post = best_time(category)

            reply = f"\n\n📊 *आज का अपडेट* ({category.capitalize()}):\n🕘 Best Time: {time_to_post}\n🎵 Audio: {audio}\n✍️ Caption: {caption}\n🏷️ Hashtags:\n{hashtags}"

            bot.send_message(chat_id=chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(chat_id=chat_id, text="कृपया `/trend fashion` या `/trend cricket` जैसे कमांड भेजें।", parse_mode=telegram.ParseMode.MARKDOWN)

    return "OK"

def send_daily():
    category = "fashion"
    caption = generate_caption(category)
    hashtags = generate_hashtags(category)
    audio = generate_audio(category)
    time_to_post = best_time(category)

    reply = f"\n\n📊 *आज का अपडेट* ({category.capitalize()}):\n🕘 Best Time: {time_to_post}\n🎵 Audio: {audio}\n✍️ Caption: {caption}\n🏷️ Hashtags:\n{hashtags}"
    bot.send_message(chat_id=CHAT_ID, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)

def run_schedule():
    schedule.every().day.at("19:00").do(send_daily)
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

if __name__ == "__main__":
    print("✅ Sohail Trend Bot Running")
    app.run(host="0.0.0.0", port=10000)
