from flask import Flask, request
import telegram
import os
import schedule
import threading
import time
import openai
import random
from datetime import datetime

# Load Env Variables
BOT_TOKEN = "7883457826:AAGEZ72ipQTpRrECa1Rzpmi_TSvrqgtnB44"
CHAT_ID = "6544146670"
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = telegram.Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Sample Hashtags and Music (refreshing logic)
hashtag_categories = {
    "fashion": ["#OOTD", "#StyleGoals", "#FashionInspo", "#StreetStyle", "#TrendyLook", "#LookBook", "#FashionGram", "#OutfitIdeas", "#StyleInspo", "#MensWear", "#WomensFashion", "#WardrobeGoals", "#SustainableStyle", "#DesiLook", "#RunwayVibes"],
    "fitness": ["#FitnessGoals", "#WorkoutDaily", "#FitInspiration", "#GymTime", "#TrainHard", "#BodyTransformation", "#CardioKing", "#YogaMood", "#HealthyVibes", "#MuscleGain", "#FitFam", "#SweatItOut", "#DailyPush", "#BeStronger", "#NoExcuses"],
    "food": ["#FoodieLife", "#TastyTreat", "#HomeChef", "#QuickRecipes", "#SpicyBites", "#FoodGoals", "#HealthyEating", "#DesiSwag", "#VeganVibes", "#CookingLove", "#Yummylicious", "#SweetTooth", "#FoodInspo", "#RecipeOfTheDay", "#FlavorBlast"],
    "default": ["#Reels", "#ExplorePage", "#InstaDaily", "#ViralReels", "#CreatorsOfInstagram", "#InstaTrend", "#ForYouPage", "#ContentCreator", "#ViralVideo", "#NewTrend", "#2025Trend", "#ReelItFeelIt", "#JustPosted", "#TrendingNow", "#MustWatch"]
}

trending_music = [
    "Chaleya – Jawan", "Tum Kya Mile – Rocky Aur Rani", "Calm Down – Rema", "Heeriye – Arijit Singh", "Kesariya – Brahmastra",
    "Night Changes – One Direction", "Let Me Love You – DJ Snake", "Pasoori – Ali Sethi", "Levitating – Dua Lipa", "Aankhon Se Batana"
]

upload_timings = ["9AM", "12PM", "3PM", "6PM", "9PM"]

def generate_caption(category="default"):
    prompt = f"Write a short, catchy Instagram reel caption about {category}. Make it trendy, engaging, and under 20 words."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "🔥 Make your moment count!"

def build_trend_message(category="default"):
    hashtags = random.sample(hashtag_categories.get(category, hashtag_categories["default"]), 15)
    music = random.choice(trending_music)
    timing = random.choice(upload_timings)
    caption = generate_caption(category)

    message = f"""📊 आज का अपडेट [{category.title()}]:
🕘 Best Time: {timing}
🎵 Trending Audio: {music}
📝 Caption Idea: {caption}
🏷️ Hashtags:
{' '.join(hashtags)}"""
    return message

@app.route('/')
def home():
    return "✅ Sohail Trend Bot Running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"]["text"].strip()

        if user_msg.startswith("/trend"):
            parts = user_msg.split()
            category = parts[1].lower() if len(parts) > 1 else "default"
            message = build_trend_message(category)
            bot.send_message(chat_id=chat_id, text=message)

    return "OK"

# Daily 7PM Message
def send_daily_update():
    today_category = random.choice(list(hashtag_categories.keys()))
    message = build_trend_message(today_category)
    bot.send_message(chat_id=CHAT_ID, text=message)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("19:00").do(send_daily_update)
threading.Thread(target=run_schedule).start()

# Run the Flask app
if __name__ == "__main__":
    print("✅ Sohail Trend Bot Running Live")
    app.run(host="0.0.0.0", port=10000)
