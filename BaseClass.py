import time
from loguru import logger
from SeleniumBaseClass import SeleniumBaseClass


class BaseClass(SeleniumBaseClass):

    def __init__(self):
        super().__init__(headless=False, browser='Chrome')

    def run_main_page(self):
        self.driver.get('http://google.com')



