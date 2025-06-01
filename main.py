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
        f"You are an expert Instagram content strategist for the Indian audience. Based on current real-time trends, generate content for this category: {category}. Respond strictly in this format:\n"
        f"\n📊 Aaj ka update [{category.capitalize()}]:\n"
        f"🕘 Best Time: [Insert India-based best time to upload]\n"
        f"📝 Caption: [Write in Hinglish – Hindi in Roman script only. Focus on reward/success. No risk or negativity.] \n"
        f"🏷️ Hashtags: #tag1 #tag2 ... (15–20 trending, India-relevant hashtags only)\n"
        f"💬 Extra Tip: [Write one short Hinglish line as a daily comment idea or hashtag trick to boost reel engagement. Must be fresh and change every time]"
        f"\nStrict Rules:\n- Do NOT include English or Western songs.\n- Caption must be Hinglish (Roman Hindi), short and catchy.\n- Avoid words like 'risk', 'danger', 'gamble'. Focus on celebration, reward, and positivity.\n- Extra Tip must feel like a smart comment idea or fresh hashtag use trick.\n- Format should remain clean and short. Do not exceed specified structure."
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
