import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InputFile

ID = 694104488
API_TOKEN = '5711898523:AAFPOq-jx1y8DVqDIdpNcSJ3iPEo6Zbn0b0'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def send_to_telgram(text: str):
    async def send_message():
        try:
            await bot.send_message(ID, text=text)

        except Exception as e:
            print(e)

    asyncio.run(send_message())