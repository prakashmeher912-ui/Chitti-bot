import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAELa2WOFxcfhx0l6W_rHTeb6b7OYB9u_6A'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Chitti AI is Live!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        # Stable AI Link
        url = "https://api.pawan.krd/v1/chat/completions"
        headers = {
            "Authorization": "Bearer pk-RskIFrIPrKovkPZpYyXoBfXyYfXyYfXyYfXyYfXyYfXyYfXy",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": m.text}]
        }
        
        r = requests.post(url, headers=headers, json=data).json()
        
        if 'choices' in r:
            res = r['choices'][0]['message']['content']
            bot.reply_to(m, res)
            
            # Voice Message
            try:
                tts = gTTS(text=res, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as v:
                    bot.send_voice(m.chat.id, v)
                os.remove("v.mp3")
            except: pass
        else:
            bot.reply_to(m, "Main sun raha hoon, kahiye!")
            
    except Exception as e:
        bot.reply_to(m, "Ek baar phir se likhiye.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
