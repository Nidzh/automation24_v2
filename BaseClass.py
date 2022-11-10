import datetime
import time
from loguru import logger
from selenium.webdriver.common.by import By

from SeleniumBaseClass import SeleniumBaseClass


class BaseClass(SeleniumBaseClass):

    def __init__(self, headless, articles: list):
        super().__init__(headless, browser='Chrome')
        self.URL = 'https://www.automation24.de/'
        self.articles = articles
        self.result_dict = {}

    def run_main_page(self):
        self.driver.get(self.URL)
        self.sleep(3)
        self.find_element_by_class_name('newdesign pull-right').click()
        self.sleep(5)
        print(f'Начало цикла - {datetime.datetime.now()}')
        for article in self.articles:
            self.article_iteration(article)
        print(f'Конец цикла - {datetime.datetime.now()}')

    def article_iteration(self, article):
        self.driver.save_screenshot('a.png')
        self.driver.find_element(By.CLASS_NAME, 'form-control').clear()
        self.driver.find_element(By.CLASS_NAME, 'form-control').send_keys(article)
        self.sleep(7)
        try:
            article_box_list = self.driver.find_element(By.CLASS_NAME, 'articles')\
                                    .find_elements(By.CLASS_NAME, 'clearfix')
            for _ in article_box_list:
                if article in _.text:
                    _.click()
                    self.sleep(1)
                    self.collect_article_data(article)
                    break
        except Exception:
            pass

    def collect_article_data(self, article):
        title = self.driver.find_element(By.TAG_NAME, 'h1').text
        price = float(self.driver.find_element(By.CLASS_NAME, 'price').find_elements(By.CSS_SELECTOR, '*')[0].get_attribute('content'))
        # discount = self.driver.find_element(By.CLASS_NAME, 'price-saving')
        # aviability = self.driver.find_element(By.CLASS_NAME, 'col-lg-5 col-md-6')

        self.result_dict[article] = (title, price)

