import datetime
import time
from BaseClass import BaseClass
from pathlib import Path
from loguru import logger
import pylightxl as xl


def excel_in(filename: str) -> list:
    db = xl.readxl(fn=filename)
    column = db.ws(ws='Прайс').col(col=1)
    return column[1:]


def excel_out(dict: dict, filename: str):
    # read in an existing worksheet and change values of its cells (same worksheet as above)
    db = xl.readxl(fn=filename)
    columnA = db.ws(ws='Прайс').col(col=1)
    db.ws(ws='Прайс').update_index(row=1, col=1, val='Артикул')
    db.ws(ws='Прайс').update_index(row=1, col=2, val='Наименование')
    db.ws(ws='Прайс').update_index(row=1, col=3, val='Стоимость')
    db.ws(ws='Прайс').update_index(row=1, col=4, val='Скидка')
    db.ws(ws='Прайс').update_index(row=1, col=5, val='Наличие')

    for key, value in dict.items():
        for row in columnA:
            if key == row:
                i = columnA.index(key) + 1
                db.ws(ws='Прайс').update_index(row=i, col=2, val=value[0])
                db.ws(ws='Прайс').update_index(row=i, col=3, val=value[1])
                # db.ws(ws='Прайс').update_index(row=i, col=4, val=value[2])
                # db.ws(ws='Прайс').update_index(row=i, col=5, val=value[3])

    xl.writexl(db=db, fn='out.xlsx')


def auto24_parser(articles: list):
    # Запуск парсера
    logger.add(Path.cwd() / 'logs' / 'logs.log', level='DEBUG')
    logger.info('Запуск парсера...')

    window = BaseClass(headless=False, articles=articles)

    try:
        window.run_main_page()
    except Exception as e:
        print(e)
    finally:
        window.driver.close()

    return window.result_dict


def get_parsing_time(filename: str):
    db = xl.readxl(fn=filename)
    column = db.ws(ws='Прайс').col(col=1)
    lenght = len(column[1:])
    sec =  lenght * 12 + 90
    return lenght, str(datetime.timedelta(seconds=sec))



def run_parser(filename: str):

    articles = excel_in(filename)
    result_dict = auto24_parser(articles)
    excel_out(result_dict, filename)
