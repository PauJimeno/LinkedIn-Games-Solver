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
    def __init__(self, queens_url):
        self.url = queens_url
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

    def get_board_number(self, class_name):
        web_element = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        ).get_attribute('innerHTML')

        board_name = web_element.strip().split()[-1]

        return board_name

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
                print(f"No 'Play' button with id={button_id} found, trying with next available id")
                pass

        if not button_found:
            raise Exception("Main game page inaccessible (Play Button not found)")

    def get_queens_board(self, main_div_id='queens-grid', board_div_class='queens-grid-no-gap'):
        board = {}

        div = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.ID, main_div_id))
        )
        div_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(div_content, 'html.parser')
        queens_grid_div = soup.find('div', class_=board_div_class)
        rows, cols = self.get_board_size(queens_grid_div)
        cell_colors = self.parse_board_content(queens_grid_div, rows, cols)

        board['rows'] = rows
        board['cols'] = cols
        board['board'] = cell_colors

        return board

    def close_web_driver(self):
        self.web_driver.quit()

    @staticmethod
    def get_board_size(board_div):
        style = board_div.get('style')
        rows = int(re.search(r'--rows: (\d+);', style).group(1))
        cols = int(re.search(r'--cols: (\d+)', style).group(1))
        return rows, cols

    @staticmethod
    def parse_board_content(board_div, rows, columns):
        board = []
        cell_divs = board_div.find_all('div', class_='queens-cell-with-border')
        current_cell = 0
        for i in range(rows):
            row = []
            for j in range(columns):
                cell_color = cell_divs[current_cell].get('class')[1].split('-')[2]
                row.append(cell_color)
                current_cell += 1
            board.append(row)
        return board







