import time
import logging
from config import TOKEN, HELP
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from urllib.request import urlopen
import json

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True,
one_time_keyboard=True)
button_1 = KeyboardButton('/help')
button_2 = KeyboardButton('/location')
kb.add(button_1).insert(button_2)

async def on_startup(_):
    print('Запуск бота.')


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, res=False):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')

    await message.reply(f'<em><b>Привет, {user_full_name}. Я персональный робот. Используй /help, чтобы узнать доступные команды.</b></em>', 
    parse_mode="HTML",
    reply_markup=kb)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message, res=False):
    await message.reply(text=HELP, 
    parse_mode="HTML", 
    reply_markup=kb)

@dp.message_handler(commands=['location'])
async def get_location(message: types.Message, res=False):
    latitude, longitude, city = get_coord()
    await message.answer(f'<em><b>Я угадываю твое местоположение. Город: {city}. Если я не прав, то ладно, тебя сложно найти.</b></em>', parse_mode="HTML")
    await bot.send_location(chat_id=message.chat.id, latitude=latitude, longitude=longitude)
    
def get_coord():
    data = get_ip()
    latitude = data['loc'].split(',')[0]
    longitude = data['loc'].split(',')[1]
    city = data['city']
    return latitude, longitude, city

def get_ip():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)
    

@dp.message_handler(content_types=["text"])
async def handle_text(message: types.Message, res=False): 
    user_full_name = message.from_user.full_name
    await message.reply(f'<em><b>Зачем ты, {user_full_name}, мне это "{message.text}" пишешь?!</b></em>', parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)