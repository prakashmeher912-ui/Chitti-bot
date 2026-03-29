import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG (Aapka Token aur Key) ---
TOKEN = '8636349817:AAELa2WOFxcfhx0l6W_rHTeb6b7OYB9u_6A'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Chitti Voice Bot is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    # Sirf Chat aur Voice Logic
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json"
        }
        
        # Fast model 'llama3-8b-8192' use kar rahe hain taaki 'Busy' na dikhaye
        data = {
            "model": "llama3-8b-8192", 
            "messages": [
                {"role": "system", "content": "Aap Chitti AI hain. Hinglish mein short aur friendly jawab dein."},
                {"role": "user", "content": m.text}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data).json()
        
        if 'choices' in response:
            res = response['choices'][0]['message']['content']
            
            # 1. Pehle Text Reply bhejo
            bot.reply_to(m, res)
            
            # 2. Fir Voice Message banao aur bhejo
            try:
                tts = gTTS(text=res, lang='hi')
                tts.save("reply.mp3")
                with open("reply.mp3", "rb") as audio:
                    bot.send_voice(m.chat.id, audio)
                os.remove("reply.mp3")
            except Exception as e:
                print(f"Voice Error: {e}")
                
        else:
            bot.reply_to(m, "Maaf kijiye, AI abhi reply nahi de paa raha hai.")
            
    except Exception as e:
        print(f"Error: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
    
