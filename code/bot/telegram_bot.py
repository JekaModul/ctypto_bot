from telegram import Bot
from telegram.error import NetworkError


TOKEN = '6599507407:AAGP6zJGdOgosBjNJu9pMc74ZhDAWvpxnV8'
bot = Bot(TOKEN)


async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=631187759, text=message, parse_mode='HTML')  # Отправка сообщения с использованием асинхронности
    except NetworkError:
        print('Произошла ошибка сети. Сообщение не было отправлено.')
