import re
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, url):
        self.url = url
        self.web_driver = None

    def set_up_driver(self):
        service = Service(GeckoDriverManager().install())
        self.web_driver = webdriver.Firefox(service=service)
        self.web_driver.get(self.url)

    def check_iframe(self):
        try:
            iframe = self.web_driver.find_element(By.TAG_NAME, 'iframe')
            self.web_driver.switch_to.frame(iframe)
        except:
            pass

    def access_main_page(self, known_button_ids):
        button_found = False
        for button_id in known_button_ids:
            try:
                button = WebDriverWait(self.web_driver, 0.5).until(
                    EC.element_to_be_clickable((By.ID, button_id))
                )
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    button_found = True
                    break
            except TimeoutException:
                pass

        if not button_found:
            raise Exception("Main game page inaccessible (Play Button not found)")

    def get_board_number(self, class_name):
        web_element = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        ).get_attribute('innerHTML')

        board_name = web_element.strip().split()[-1]

        return board_name

    def close_web_driver(self):
        self.web_driver.quit()
