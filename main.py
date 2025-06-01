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
def get_trend_update():
    prompt = (
        "You are a professional social media trend expert. Generate a mixed list of 20–25 unique items optimized for Instagram Reels and Shorts viral growth. Each item must be unique and must belong to one of these 7 categories:\n"
        "1. Cricket-related trending hashtags\n"
        "2. Cricket meme hashtags\n"
        "3. Cricket reel/video captions\n"
        "4. Best time to upload cricket content (India based, 90%+ reach chance)\n"
        "5. Casino trending hashtags\n"
        "6. Satta/betting trending hashtags\n"
        "7. Currently trending reel audio/music (short format, reel-friendly)\n"
        "\n"
        "Rules:\n"
        "- No repetition.\n"
        "- All content must be based on today's real-time global trends.\n"
        "- Keep language casual, engaging, and optimized for reach.\n"
        "- Avoid long explanations, only the trending content in list format.\n"
        "\n"
        "Output:")

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

        if user_msg == "/trend" or user_msg.startswith("/trend "):
            trend_message = get_trend_update()
            bot.send_message(chat_id=chat_id, text=trend_message)

    return "OK"

# 🚀 Run Flask App
if __name__ == "__main__":
    print("✅ Sohail Trend Bot Running")
    app.run(host="0.0.0.0", port=10000)
