import json
import os
import random
import time
from pathlib import Path

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class SeleniumBaseClass:

    def __init__(self, headless=False, browser: str = 'Chrome'):
        self.browser = browser.capitalize()
        os.environ['GH_TOKEN'] = "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"

        match self.browser:
            case 'Chrome':
                self.options = uc.ChromeOptions()
                if headless == True:
                    self.options.headless = True
                    self.options.add_argument("--headless")
                    # self.options.add_argument("--no-sandbox")
                    # self.options.add_argument("--disable-gpu")
                self.options.add_argument("--start-maximized")
                self.driver = uc.Chrome(options=self.options)
                # self.driver.maximize_window()

            case 'Edge':
                from selenium.webdriver.edge.service import Service
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

            case 'Opera':
                from webdriver_manager.opera import OperaDriverManager
                self.options = webdriver.ChromeOptions()
                self.options.add_argument('allow-elevated-browser')
                self.options.binary_location = "/usr/bin/opera"
                self.driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=self.options)

            case 'Firefox':
                from selenium.webdriver.firefox.service import Service
                from webdriver_manager.firefox import GeckoDriverManager
                self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

            case 'Brave':
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.utils import ChromeType
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))

    # ____________ Navigation ____________
    def find_elements_by_class_name(self, value: str):
        return self.driver.find_elements(By.XPATH, f"//*[@class='{value}']")

    def find_element_by_class_name(self, value: str):
        return self.driver.find_element(By.XPATH, f"//*[@class='{value}']")

    def scroll_page(self):
        html = self.driver.find_element(by=By.TAG_NAME, value='html')
        while True:
            size = self.driver.execute_script("return document.body.scrollHeight", html)
            html.send_keys(Keys.END)
            time.sleep(2)
            new_size = self.driver.execute_script("return document.body.scrollHeight", html)
            if new_size == size:
                break

    # ____________ Save & Load data ____________

    def get_html_file(self, file_name: str):
        filepath = Path.cwd() / 'html' / f'{file_name}.html'
        with filepath.open('w') as f:
            f.write(self.driver.page_source)

    def get_cookies(self, sleep_time: int = 5):
        time.sleep(sleep_time)
        file = self.driver.get_cookies()

        filepath = Path.cwd() / 'cookie' / 'cookie.json'
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open('w', encoding='UTF-8') as f:
            json.dump(file, f)

    def set_cookies(self):
        filepath = Path.cwd() / 'cookie' / 'cookie.json'
        with filepath.open('r', encoding='UTF-8') as f:
            cookie_list = json.load(f)
            for cookie in cookie_list:
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def get_local_storage_dump(self, sleep_time: int = 5):
        time.sleep(sleep_time)
        file = self.driver.execute_script(
            "var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items; ")

        filepath = Path.cwd() / 'localstorage' / 'localstorage.json'
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open('w', encoding='UTF-8') as f:
            json.dump(file, f)

    def set_local_storage_dump(self):
        filepath = Path.cwd() / 'localstorage' / 'localstorage.json'
        with filepath.open('r', encoding='UTF-8') as f:
            dict = json.load(f)
            for key, value in dict.items():
                self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)
        time.sleep(2)
        self.driver.refresh()

    def sleep(self, delay=0):
        sleep_time = random.random()
        time.sleep(sleep_time + delay)
