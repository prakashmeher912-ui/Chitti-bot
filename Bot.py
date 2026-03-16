import telebot
import requests
import os
from gtts import gTTS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
TOKEN = '8636349817:AAEIyvx_vi0_M9-DfsaCSEMEiXB2LeWHxZo'
GROQ_KEY = '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'
ADMIN_ID = 7830250520 

bot = telebot.TeleBot(TOKEN)
USER_FILE = "users_list.txt"

def save_user(message):
    uid, name = message.from_user.id, message.from_user.first_name
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: data = f.read()
    if str(uid) not in data:
        with open(USER_FILE, "a") as f: f.write(f"ID: {uid} | Name: {name}\n")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message)
    name = "Prakash Malik" if message.from_user.id == ADMIN_ID else message.from_user.first_name
    bot.reply_to(message, f"Pranam {name}! Main Chitti hoon, mere owner PRAKASH hain.")

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id == ADMIN_ID:
        if os.path.exists(USER_FILE) and os.path.getsize(USER_FILE) > 0:
            with open(USER_FILE, "r") as f: data = f.read()
            bot.send_message(message.chat.id, f"👥 **Users List:**\n\n{data}")
        else: bot.send_message(message.chat.id, "List khali hai.")
    else: bot.send_message(message.chat.id, "Sirf Prakash Malik ke liye hai.")

@bot.callback_query_handler(func=lambda call: call.data == "speak")
def voice(call):
    try:
        tts = gTTS(text=call.message.text[:500], lang='hi', slow=False)
        tts.save("v.mp3")
        with open("v.mp3", "rb") as a: bot.send_voice(call.message.chat.id, a)
        os.remove("v.mp3")
    except: pass

@bot.message_handler(func=lambda message: True)
def chat(message):
    save_user(message)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Name: Chitti. Owner: PRAKASH. Language: Hindi. Short replies."}, {"role": "user", "content": message.text}]}
        res = requests.post(url, headers={"Authorization": f"Bearer {GROQ_KEY}"}, json=payload).json()
        ans = res['choices'][0]['message']['content']
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔊 Suniye", callback_data="speak"))
        bot.send_message(message.chat.id, ans, reply_markup=markup)
    except: pass

bot.infinity_polling()
