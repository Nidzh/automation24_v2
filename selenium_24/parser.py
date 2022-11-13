import datetime
from pathlib import Path

import pylightxl as xl
from loguru import logger

from selenium_24.BaseClass import BaseClass


class Auto24Parser:

    def __init__(self, input_fl: Path, output_fl: Path):
        self.input_fl = input_fl
        self.output_fl = output_fl
        self.articles = []
        self.result_dict = {}

    def auto24_parser(self):
        logger.add(Path.cwd() / 'logs' / 'logs.log', level='DEBUG')
        logger.info('Запуск парсера...')

        window = BaseClass(articles=self.articles)

        try:
            window.run_main_page()
            self.result_dict = window.result_dict
        except Exception as e:
            print(e)
        finally:
            window.driver.close()

    def get_parsing_time(self):
        db = xl.readxl(fn=self.input_fl)
        column = db.ws(ws='Прайс').col(col=1)
        lenght = len(column[1:])
        sec = lenght * 12 + 90
        return lenght, str(datetime.timedelta(seconds=sec))

    def excel_in(self):
        db = xl.readxl(fn=self.input_fl)
        column = db.ws(ws='Прайс').col(col=1)
        self.articles = column[1:]

    def excel_out(self):
        db = xl.readxl(fn=self.input_fl)
        columnA = db.ws(ws='Прайс').col(col=1)
        db.ws(ws='Прайс').update_index(row=1, col=1, val='Артикул')
        db.ws(ws='Прайс').update_index(row=1, col=2, val='Наименование')
        db.ws(ws='Прайс').update_index(row=1, col=3, val='Стоимость')
        db.ws(ws='Прайс').update_index(row=1, col=4, val='Скидка')
        db.ws(ws='Прайс').update_index(row=1, col=5, val='Наличие')

        for key, value in self.result_dict.items():
            for row in columnA:
                if key == row:
                    i = columnA.index(key) + 1
                    db.ws(ws='Прайс').update_index(row=i, col=2, val=value[0])
                    db.ws(ws='Прайс').update_index(row=i, col=3, val=value[1])
                    # db.ws(ws='Прайс').update_index(row=i, col=4, val=value[2])
                    # db.ws(ws='Прайс').update_index(row=i, col=5, val=value[3])
        self.output_fl.unlink(missing_ok=True)
        xl.writexl(db=db, fn=self.output_fl)

    def run_parser(self):
        self.excel_in()
        self.auto24_parser()
        self.excel_out()
