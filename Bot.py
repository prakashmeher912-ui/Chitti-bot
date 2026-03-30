import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAELa2WOFxcfhx0l6W_rHTeb6b7OYB9u_6A'
GEMINI_KEY = 'AIzaSyDUuqZYqXuWR2H7pUOwTDe0-_0H4jCW-HM' 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Chitti Gemini is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        # Google Gemini API Direct Call
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts":[{"text": m.text}]}]}
        
        r = requests.post(url, headers=headers, json=data).json()
        
        # Check if AI gave a response
        if 'candidates' in r and len(r['candidates']) > 0:
            res = r['candidates'][0]['content']['parts'][0]['text']
            # 1. Text Reply
            bot.reply_to(m, res)
            
            # 2. Voice Reply
            try:
                tts = gTTS(text=res, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as v: bot.send_voice(m.chat.id, v)
                os.remove("v.mp3")
            except: pass
        else:
            # Agar API fail ho jaye
            bot.reply_to(m, "Main sun raha hoon Prakash bhai, par thoda network slow hai. Ek baar fir se poochiye!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
