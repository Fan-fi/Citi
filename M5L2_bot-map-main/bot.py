import telebot
import os
from logic import MapBot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
mapper = MapBot()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "🌍 Привет! Я показываю любой город на карте мира.\n"
        "Просто напиши название города на английском.\n"
        "Например: london, paris, tokyo, moscow")

@bot.message_handler(content_types=['text'])
def show_city(message):
    city_name = message.text.strip()
    
    if not city_name:
        return
    
    # Ищем в БД
    city_data = mapper.find_city(city_name)
    
    if not city_data:
        bot.send_message(message.chat.id,
            f"❌ Город '{city_name}' не найден в базе.\n"
            "Проверь написание на английском.")
        return
    
    name, lat, lon = city_data
    
    # Сообщаем что рисуем
    msg = bot.send_message(message.chat.id, f"📍 Ищу {name}...")
    
    # Рисуем карту
    try:
        image_path = mapper.draw_city_on_world_map(name, lat, lon)
        
        # Отправляем карту
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo,
                          caption=f"Широта: {lat:.4f}\nДолгота: {lon:.4f}")
        
        # Удаляем временный файл
        os.remove(image_path)
        
        # Удаляем сообщение "Ищу..."
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен. Готов показывать города!")
    bot.polling()