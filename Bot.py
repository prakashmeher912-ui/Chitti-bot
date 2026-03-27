import telebot, requests, os, threading, urllib.parse, sqlite3
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAEOsDfb0I-jHPnyr-JZEYTiHyWr7mH9STI'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- MEMORY DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                 (user_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_memory(user_id, role, content):
    conn = sqlite3.connect('memory.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_history VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()

def get_memory(user_id):
    conn = sqlite3.connect('memory.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history WHERE user_id=? ORDER BY ROWID DESC LIMIT 5", (user_id,))
    rows = c.fetchall()
    conn.close()
    # Purani 5 baatein yaad rakhega
    history = [{"role": r, "content": c} for r, c in reversed(rows)]
    return history

@app.route('/')
def home(): return "Chitti with Memory is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    query = m.text.lower()
    user_id = m.from_user.id
    
    # 1. PHOTO FEATURE
    if any(word in query for word in ["photo", "image", "banao"]):
        prompt = query.replace("photo", "").replace("image", "").replace("banao", "").strip()
        if prompt:
            bot.reply_to(m, f"Main '{prompt}' ki photo bana raha hoon...")
            bot.send_photo(m.chat.id, f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}")
            return

    # 2. YOUTUBE FEATURE
    if any(word in query for word in ["gaana", "song", "video"]):
        song = query.replace("gaana", "").replace("song", "").strip()
        if song:
            bot.reply_to(m, f"Link: https://www.youtube.com/results?search_query={urllib.parse.quote(song)}")
            return

    # 3. CHAT WITH MEMORY
    try:
        # Purani yaadein nikaalna
        history = get_memory(user_id)
        history.append({"role": "user", "content": m.text})
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}"}
        system_msg = {"role": "system", "content": "Aap Chitti AI hain. Aapko purani baatein yaad rakhni hain aur Hinglish mein jawab dena hai."}
        
        data = {"model": "llama-3.3-70b-versatile", "messages": [system_msg] + history}
        
        response = requests.post(url, headers=headers, json=data).json()
        
        if 'choices' in response:
            res = response['choices'][0]['message']['content']
            bot.reply_to(m, res)
            
            # Memory save karna
            save_memory(user_id, "user", m.text)
            save_memory(user_id, "assistant", res)
            
            # Voice
            tts = gTTS(text=res, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v: bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
    except: pass

if __name__ == "__main__":
    init_db()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
