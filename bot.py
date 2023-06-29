from io import BytesIO
import telebot
from config import TOKEN
from prediction import get_predict

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Привет! Я бот, который может проверить болезнь растений по фото. Просто отправь мне фотографию.')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем информацию о фото
        file_info = bot.get_file(message.photo[-1].file_id)
        file_path = file_info.file_path
        
        # Скачиваем фото
        downloaded_file = bot.download_file(file_path)

        prediction = get_predict(BytesIO(downloaded_file))
        
        # Отправляем ответ пользователю
        bot.reply_to(message, prediction)
    
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла ошибка при обработке фото.')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, 'Нужно отправить фото!')

bot.polling()