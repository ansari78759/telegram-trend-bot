from flask import Flask, request
import telegram
import os
import openai

# 📦 Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telegram.Bot(token=BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# 🧠 GPT (o4-mini) से Trend Content Generate Function
def get_trend_update(category):
    prompt = (
        f"You are a professional Instagram Reels expert. Based on current real-time trends, generate content for this category: {category}. Respond strictly in this format:\n"
        f"\n📊 आज का अपडेट [{category.capitalize()}]:\n"
        f"🕘 Best Time: [Insert India-based best time to upload]\n"
        f"🎵 Trending Audio: [Insert currently trending audio/song name] (reel-friendly)\n"
        f"📝 Caption: [Short, fun, creative line — must be reward-focused only, never mention risk] \n"
        f"🏷️ Hashtags: #tag1 #tag2 ... (15–20 trending & relevant hashtags only)\n"
        f"\nStrict rules:\n- Never repeat hashtags or sections\n- Do NOT include words like 'risk', 'danger', 'gamble' in captions. Only talk about reward/success/fun/luxury\n- Language should be sharp and optimized for reach\n- Never exceed the format above"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
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

        if user_msg.startswith("/trend"):
            parts = user_msg.split(" ")
            if len(parts) > 1:
                category = parts[1]
            else:
                category = "cricket"

            trend_message = get_trend_update(category)
            bot.send_message(chat_id=chat_id, text=trend_message)

    return "OK"

# 🚀 Start Flask App (for local or gunicorn)
if __name__ == "__main__":
    print("✅ Sohail Trend Bot Running")
    app.run(host="0.0.0.0", port=10000)
    
