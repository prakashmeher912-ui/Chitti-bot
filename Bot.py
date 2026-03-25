import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- AAPKA UPDATED CONFIG ---
TOKEN = '8636349817:AAEOsDfb0I-jHPnyr-JZEYTiHyWr7mH9STI'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Chitti is Running!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile", 
            "messages": [
                {"role": "system", "content": "Aap Chitti AI hain. Hinglish mein jawab dein (English letters mein Hindi)."},
                {"role": "user", "content": m.text}
            ]
        }
        r = requests.post(url, headers=headers, json=data).json()
        if 'choices' in r:
            res = r['choices'][0]['message']['content']
            bot.reply_to(m, res)
            tts = gTTS(text=res, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v:
                bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
    except Exception as e: print(f"Error: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.polling()
    
