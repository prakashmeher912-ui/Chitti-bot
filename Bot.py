import telebot, requests, os, threading
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAEOsDfb0I-jHPnyr-JZEYTiHyWr7mH9STI'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Chitti is Online"

@bot.message_handler(func=lambda m: True)
def handle(m):
    text = m.text.lower()
    
    # --- FEATURE: IMAGE GENERATION ---
    if text.startswith("photo") or text.startswith("image") or text.startswith("banao"):
        try:
            prompt = text.replace("photo", "").replace("image", "").replace("banao", "").strip()
            if not prompt:
                bot.reply_to(m, "Kiski photo banau? Likho: 'photo of a cat'")
                return
                
            bot.reply_to(m, f"Theek hai, main '{prompt}' ki photo bana raha hoon...")
            image_url = f"https://image.pollinations.ai/prompt/{prompt}"
            bot.send_photo(m.chat.id, image_url)
            return
        except:
            bot.reply_to(m, "Photo banane mein kuch dikkat hui.")
            return

    # --- FEATURE: CHAT & VOICE (Already working) ---
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile", 
            "messages": [
                {"role": "system", "content": "Aap Chitti AI hain. Hinglish mein jawab dein (English letters mein Hindi). Friendly rahein."},
                {"role": "user", "content": m.text}
            ]
        }
        
        response_json = requests.post(url, headers=headers, json=data).json()
        
        # Checking for KeyError Fix
        if 'choices' in response_json:
            res = response_json['choices'][0]['message']['content']
            bot.reply_to(m, res)
            
            # Voice Message
            tts = gTTS(text=res, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v:
                bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
        else:
            bot.reply_to(m, "AI ne jawab nahi diya, shayad limit khatam ho gayi.")
            
    except Exception as e:
        print(f"Error: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.polling()
    
