import telebot, requests, os, threading, urllib.parse
from gtts import gTTS
from flask import Flask

# --- CONFIG (Token aur Key ekdum sahi hain) ---
TOKEN = '8636349817:AAEOsDfb0I-jHPnyr-JZEYTiHyWr7mH9STI'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Chitti AI is Online and Running!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    query = m.text.lower()
    
    # 1. PHOTO GENERATION FEATURE
    if any(word in query for word in ["photo", "image", "banao", "pic"]):
        prompt = query.replace("photo", "").replace("image", "").replace("banao", "").replace("pic", "").strip()
        if prompt:
            bot.reply_to(m, f"Theek hai, main '{prompt}' ki photo bana raha hoon... Thoda rukiye.")
            image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
            bot.send_photo(m.chat.id, image_url)
            return

    # 2. YOUTUBE SEARCH FEATURE
    if any(word in query for word in ["gaana", "song", "video", "youtube"]):
        song_name = query.replace("gaana", "").replace("song", "").replace("video", "").replace("youtube", "").strip()
        if song_name:
            encoded_name = urllib.parse.quote(song_name)
            yt_link = f"https://www.youtube.com/results?search_query={encoded_name}"
            bot.reply_to(m, f"Aapke liye gaana mil gaya: {yt_link}")
            return

    # 3. CHAT & VOICE FEATURE (With Error Handling)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile", 
            "messages": [
                {"role": "system", "content": "Aap Chitti AI hain. Aap hamesha Hinglish mein jawab denge (Hindi words in English letters). Friendly rahein aur maalik ka naam baar baar na lein."},
                {"role": "user", "content": m.text}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data).json()
        
        # Check if AI gave a valid response
        if 'choices' in response:
            res = response['choices'][0]['message']['content']
            bot.reply_to(m, res)
            
            # Create Voice Message
            tts = gTTS(text=res, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v:
                bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
        else:
            bot.reply_to(m, "Maaf kijiyega, abhi AI busy hai. Thodi der baad try karein!")
            
    except Exception as e:
        print(f"Error occurred: {e}")

def run_flask():
    # Render ke liye port 10000 zaroori hai
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Flask aur Bot dono ko saath chalane ke liye threading
    threading.Thread(target=run_flask).start()
    print("CHITTI IS STARTING...")
    bot.infinity_polling()
        
