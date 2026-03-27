import telebot, requests, os, threading, urllib.parse
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
    query = m.text.lower()
    
    # --- FEATURE 1: PHOTO GENERATION ---
    if any(word in query for word in ["photo", "image", "banao", "pic"]):
        prompt = query.replace("photo", "").replace("image", "").replace("banao", "").strip()
        if prompt:
            bot.reply_to(m, f"Theek hai, main '{prompt}' ki photo bana raha hoon...")
            image_url = f"https://image.pollinations.ai/prompt/{prompt}"
            bot.send_photo(m.chat.id, image_url)
            return

    # --- FEATURE 2: YOUTUBE SEARCH ---
    if any(word in query for word in ["gaana", "song", "video", "youtube"]):
        song_name = query.replace("gaana", "").replace("song", "").replace("video", "").strip()
        if song_name:
            encoded_name = urllib.parse.quote(song_name)
            yt_link = f"https://www.youtube.com/results?search_query={encoded_name}"
            bot.reply_to(m, f"Aapke liye gaana mil gaya: {yt_link}")
            return

    # --- FEATURE 3: CHAT & VOICE ---
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Aap Chitti AI hain. Hinglish mein jawab dein."}, {"role": "user", "content": m.text}]}
        
        r = requests.post(url, headers=headers, json=data).json()
        if 'choices' in r:
            res = r['choices'][0]['message']['content']
            bot.reply_to(m, res)
            tts = gTTS(text=res, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v:
                bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
    except:
        pass

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.polling()
            
