import telebot, requests, os, threading, urllib.parse, sqlite3
from gtts import gTTS
from flask import Flask

# --- CONFIG ---
TOKEN = '8636349817:AAEOsDfb0I-jHPnyr-JZEYTiHyWr7mH9STI'
KEY = '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'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- MEMORY SYSTEM (Database) ---
def init_db():
    conn = sqlite3.connect('chitti_memory.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory 
                 (user_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_to_memory(user_id, role, content):
    conn = sqlite3.connect('chitti_memory.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO memory VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = sqlite3.connect('chitti_memory.db', check_same_thread=False)
    c = conn.cursor()
    # Aakhri 10 baatein yaad rakhega
    c.execute("SELECT role, content FROM memory WHERE user_id=? ORDER BY ROWID DESC LIMIT 10", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": ct} for r, ct in reversed(rows)]

@app.route('/')
def home(): return "Chitti AI with Memory is Online!"

@bot.message_handler(func=lambda m: True)
def handle(m):
    query = m.text.lower()
    uid = m.from_user.id
    
    # 1. PHOTO GENERATION
    if any(x in query for x in ["photo", "image", "banao", "pic"]):
        p = query.replace("photo","").replace("image","").replace("banao","").strip()
        if p:
            bot.reply_to(m, f"Theek hai, main '{p}' ki photo bana raha hoon...")
            bot.send_photo(m.chat.id, f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}")
            return

    # 2. YOUTUBE SEARCH
    if any(x in query for x in ["gaana", "song", "video", "youtube"]):
        s = query.replace("gaana","").replace("song","").replace("video","").strip()
        if s:
            link = f"https://www.youtube.com/results?search_query={urllib.parse.quote(s)}"
            bot.reply_to(m, f"Aapke liye gaana: {link}")
            return

    # 3. CHAT WITH LONG-TERM MEMORY
    try:
        # Purani baatein yaad karna
        past_chats = get_chat_history(uid)
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
        
        system_prompt = {"role": "system", "content": "Aap Chitti AI hain. Aapko purani baatein yaad rakhni hain. Hamesha Hinglish mein jawab dein."}
        user_msg = {"role": "user", "content": m.text}
        
        messages = [system_prompt] + past_chats + [user_msg]
        
        data = {"model": "llama-3.3-70b-versatile", "messages": messages}
        
        resp = requests.post(url, headers=headers, json=data).json()
        
        if 'choices' in resp:
            answer = resp['choices'][0]['message']['content']
            bot.reply_to(m, answer)
            
            # Memory mein save karna
            save_to_memory(uid, "user", m.text)
            save_to_memory(uid, "assistant", answer)
            
            # Voice Message
            tts = gTTS(text=answer, lang='hi')
            tts.save("v.mp3")
            with open("v.mp3", "rb") as v: bot.send_voice(m.chat.id, v)
            os.remove("v.mp3")
        else:
            bot.reply_to(m, "Maaf kijiye, AI abhi busy hai.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init_db()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
