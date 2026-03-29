import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG (Aapka Naya Token) ---
TOKEN = '8636349817:AAELa2WOFxcfhx0l6W_rHTeb6b7OYB9u_6A'
# Fresh API Key for AI
KEY = 'gsk_y4M4B0n3YkS8V9L2pQ5Rz6J7H8G9F0E1D2C3B4A5' 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Chitti AI Voice Bot is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        
        # Fast Model use kar rahe hain
        data = {
            "model": "llama-3.1-8b-instant", 
            "messages": [
                {"role": "system", "content": "Aap Chitti AI hain. Hinglish mein short aur friendly jawab dein."},
                {"role": "user", "content": m.text}
            ]
        }
        
        r = requests.post(url, headers=headers, json=data).json()
        
        if 'choices' in r:
            res = r['choices'][0]['message']['content']
            # 1. Text Reply
            bot.reply_to(m, res)
            
            # 2. Voice Reply
            try:
                tts = gTTS(text=res, lang='hi')
                tts.save("v.mp3")
                with open("v.mp3", "rb") as v:
                    bot.send_voice(m.chat.id, v)
                os.remove("v.mp3")
            except:
                pass
        else:
            bot.reply_to(m, "System update ho raha hai, thodi der mein try karein.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
