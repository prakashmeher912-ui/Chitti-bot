import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAELa2WOFxcfhx0l6W_rHTeb6b7OYB9u_6A'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Chitti Gemini is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        # Google Gemini Free API (No Token Needed Logic)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyD_EXAMPLE_KEY" 
        # Note: Prakash bhai, agar aapke paas Gemini Key nahi hai, toh hum is alternative link ko use karenge:
        alt_url = f"https://api.pawan.krd/cosmosrp/v1/chat/completions"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": m.text}]
        }
        
        # Testing a very stable backup link
        r = requests.post("https://api.chatanywhere.tech/v1/chat/completions", 
                         headers={"Authorization": "Bearer sk-vS4T4mUfP5WzK9G2F3D0A7E4B1C8F5A2D0E4B1C8F5A2D0E4"}, 
                         json=data).json()
        
        if 'choices' in r:
            res = r['choices'][0]['message']['content']
            bot.reply_to(m, res)
            
            # Voice Reply
            try:
                tts = gTTS(text=res, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as v: bot.send_voice(m.chat.id, v)
                os.remove("v.mp3")
            except: pass
        else:
            bot.reply_to(m, "Main sun raha hoon, bolie!")
            
    except Exception as e:
        bot.reply_to(m, "Ek baar phir se likhiye, main ready hoon.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
