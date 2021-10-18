import asyncio
from aiogram.types.base import String
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

import soundfile as sf
import config
import logging
import random
import speech_recognition as sr
import wikipedia
import subprocess

from translate import Translator
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, File, Message, message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
const = 100
r = sr.Recognizer()

#hello

@dp.message_handler(commands="start")
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Список команд", callback_data="help"),
        types.InlineKeyboardButton(text="GitHub", url="https://github.com")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Привет! Чем могу помочь?", reply_markup=keyboard)

@dp.callback_query_handler(text='help')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, config.help_text)

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

#vtt (dont work)
'''
async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")
@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    voice = await message.voice.get_file()
    path = "/voices"

    await handle_file(file=voice, file_name=f"input.ogg", path=path)

    #data, samplerate = sf.read('/voices/voi.ogg')
    #sf.write('voices/voir.wav', data, samplerate)

    await asyncio.sleep(5)

    input_ogg = open('input.ogg')

    #data, samplerate = sf.read(input_ogg)
    #sf.write('output.wav', data, samplerate)

    await asyncio.sleep(5)

    sample_audio = sr.AudioFile('C:/voices/output.wav')
    with sample_audio as audio_file:
        sr.adjust_for_ambient_noise(audio_file)
        audio_content = sr.record(audio_file)

        await message.reply(sr.recognize_google(audio_content))
'''
#polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)