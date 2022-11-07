import time
from BaseClass import BaseClass
from pathlib import Path
from loguru import logger

if __name__ == '__main__':

    # Запуск парсера
    logger.add(Path.cwd() / 'logs' / 'logs.log', level='DEBUG')
    logger.info('Запуск парсера...')

    window = BaseClass()
    window.run_main_page()
    time.sleep(5)