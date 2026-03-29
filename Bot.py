import telebot, requests, os, threading, urllib.parse
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAEOsDfb0I-jHPnyr-JZEYTiHyWr7mH9STI'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Chitti AI is Live!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    query = m.text.lower()
    
    # 1. PHOTO/IMAGE FEATURE
    if any(word in query for word in ["photo", "image", "banao", "pic"]):
        p = query.replace("photo","").replace("image","").replace("banao","").strip()
        if p:
            bot.reply_to(m, f"Main '{p}' ki photo bana raha hoon...")
            bot.send_photo(m.chat.id, f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}")
            return

    # 2. CHAT FEATURE (Using a Faster Model)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        
        # Humne model badal kar 'llama3-8b-8192' kar diya hai (Ye fast hai)
        data = {
            "model": "llama3-8b-8192", 
            "messages": [{"role": "user", "content": m.text}]
        }
        
        r = requests.post(url, headers=headers, json=data).json()
        
        if 'choices' in r:
            res = r['choices'][0]['message']['content']
            bot.reply_to(m, res)
            
            # Voice Message
            tts = gTTS(text=res, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v: bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
        else:
            bot.reply_to(m, "AI ki limit shayad khatam ho gayi hai, main abhi sirf photos bana sakta hoon.")
    except:
        pass

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
            
