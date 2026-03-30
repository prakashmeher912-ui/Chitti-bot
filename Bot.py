import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAELa2WOFxcfhx0l6W_rHTeb6b7OYB9u_6A'
# Aapki apni Permanent Gemini Key
GEMINI_KEY = 'AIzaSyDUuqZYqXuWR2H7pUOwTDe0-_0H4jCW-HM' 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Chitti Gemini Bot is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        # Google Gemini Official API URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": m.text}]
            }]
        }
        
        # Google API ko request bhej rahe hain
        response = requests.post(url, headers=headers, json=data)
        r = response.json()
        
        if 'candidates' in r:
            res = r['candidates'][0]['content']['parts'][0]['text']
            
            # 1. Text Reply (Aapko likhkar jawab dega)
            bot.reply_to(m, res)
            
            # 2. Voice Reply (Aapko bolkar jawab dega)
            try:
                tts = gTTS(text=res, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as v:
                    bot.send_voice(m.chat.id, v)
                os.remove("v.mp3")
            except Exception as ve:
                print(f"Voice Error: {ve}")
        else:
            # Agar koi error aaye toh error message dikhayega
            bot.reply_to(m, "Maaf kijiye, main abhi samajh nahi pa raha hoon. Ek baar phir likhiye.")
            print(f"API Error: {r}")

    except Exception as e:
        print(f"General Error: {e}")

if __name__ == "__main__":
    # Render ko active rakhne ke liye Flask
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
