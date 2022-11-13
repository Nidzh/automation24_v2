import datetime
import time

from aiogram import Bot, Dispatcher, executor, types
from selenium_24.parser import run_parser, get_parsing_time

ID = 694104488
API_TOKEN = '5722453782:AAGwG4Wgfns_UCRzzJX5ztmx9O_l8yWu_nk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Приветсвую. Отправьте мне .xls файл. Я сделаю своб работу и верну ответ")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    if document := message.document:
        print(f'Запуск программмы - {datetime.datetime.now()}')
        doc_type = document.file_name.split('.')[-1]
        if doc_type in ('xlx', 'xlsx'):
            await message.answer('Загрузка файла на сервер...')
            await document.download(destination_file=document.file_name)
            time.sleep(5)
            lenght, parsing_time = get_parsing_time(document.file_name)
            await message.answer(
                f'Файл загружен. Кол-во артикулей: {lenght}. Примерное время обработки: {parsing_time}')
            run_parser(document.file_name)
            out_doc = open('out.xlsx', 'rb')
            await message.answer_document(out_doc)
    print(f'Конец программмы - {datetime.datetime.now()}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
