from scraper.Scraper import Scraper

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class WendScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def get_wend_board(self, main_div_class):
        board = {}

        div = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, main_div_class))
        )
        div_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(div_content, 'html.parser')
        wend_board_div = soup.find('div', attrs={'data-testid': 'interactive-grid'})
        wend_words_div = soup.find('div', attrs={'data-testid': 'wend-word-list'})

        size = self.get_board_size(wend_board_div)[0]
        board['size'] = size
        board.update(self.parse_board_content(wend_board_div, wend_words_div, size))

        return board

    @staticmethod
    def get_board_size(board_div):
        style = board_div.get('style', '')
        values = [int(x) for x in re.findall(r':\s*(\d+)', style)]
        rows = values[0]
        cols = values[1]

        return rows, cols

    @staticmethod
    def parse_board_content(board_div, wend_words_div, size):
        data = {'board': [['' for _ in range(size)] for _ in range(size)], 'words': []}

        # Obtain board information
        cells = board_div.find_all('div', attrs={'data-cell-idx': True})
        for cell in cells:
            idx = int(cell.get('data-cell-idx')) # Obtain cell idx
            i, j = idx // size, idx % size
            letter = cell.find('span').get_text() # Obtain cell letter
            data['board'][i][j] = letter

        # Obtain word length information
        div_attr = re.compile(r'^wend-word-list-slots-')
        words = wend_words_div.find_all('div', attrs={'data-testid': div_attr})
        for word in words:
            letters = word.find_all('div')
            data['words'].append(len(letters))

        return data
