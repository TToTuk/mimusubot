import asyncio
import config
import logging
import random
import wikipedia
import subprocess

from translate import Translator
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, File, Message, message
from aiobalaboba import balaboba

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
const = 100

#hello

@dp.message_handler(commands="start")
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Список команд", callback_data="help"),
        types.InlineKeyboardButton(text="GitHub", url="https://github.com/TToTuk/mimusubot")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Привет! Чем могу помочь?", reply_markup=keyboard)

@dp.callback_query_handler(text='help')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, config.help_text)
   
#help

@dp.message_handler(commands='help')
async def help(message):
    await message.reply(config.help_text)
    
#me
@dp.message_handler(commands=['me'])
async def me(message: types.Message):
    mesme = message.text[4:]
    await message.bot.delete_message(chat_id=message.chat.id ,message_id=message.message_id)
    if mesme.strip():
       await message.answer(message.from_user.first_name + ' ' + message.from_user.last_name + " " + mesme)
    else:
        return

#translate

@dp.message_handler(commands=['en'])
async def ru_translate(message):
    if not message.reply_to_message:
        await message.reply('Команда должна быть ответом на сообщение')
        return
    translatoren = Translator(from_lang="Russian",to_lang="English")
    await message.reply(translatoren.translate(message.reply_to_message.text))

@dp.message_handler(commands=['ru'])
async def ru_translate(message):
    if not message.reply_to_message:
        await message.reply('Команда должна быть ответом на сообщение')
        return
    translatorru = Translator(to_lang="Russian")
    await message.reply(translatorru.translate(message.reply_to_message.text))

#coin

@dp.message_handler(commands=['coin'])
async def coin(message):
    coin_chance = random.randint(0, 100)
    if coin_chance > 50:
        await message.reply_sticker(config.ST1)
    if coin_chance == 50:
        await message.reply_sticker(config.ST2)
    if coin_chance < 50:
        await message.reply_sticker(config.ST3)


#random number
@dp.message_handler(commands=['rnum'])
async def rnum(message: types.Message):
    mes = message.text[6:]
    if mes.strip():
        const = int(mes)
    else:
        const = 100
    await message.reply(random.randint(0, const))

#wiki

@dp.message_handler(commands=['wiki'])
async def wiki(message: types.Message):
    search = message.text[6:]
    print(search)
    wikipedia.set_lang('ru')
    await message.reply(wikipedia.summary(search))
    
#weather

@dp.message_handler(commands='weather')
async def help(message):
    wes = message.text[9:]
    if wes.strip():
        weconst = str(wes)
        observ = mgr.weather_at_place(weconst)
        w = observ.weather
    else:
       weconst = 'Анжеро-Судженск'
       observ = mgr.weather_at_place(weconst)
       w = observ.weather
    await message.answer('В данное время в городе '+ weconst +':\nтемпература равна ' + str(w.temperature('celsius')['temp']) + ' С,\n скорость ветра ' + str(w.wind()['speed']) + ' м/с')

#balaboba
@dp.message_handler(commands=['b'])
async def me(message: types.Message):
    mesb = message.text[3:]
    response = await balaboba(mesb)
    print(response)
    await message.reply(response)

#polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
