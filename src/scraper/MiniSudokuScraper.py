from scraper.Scraper import Scraper

from collections import defaultdict
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class MiniSudokuScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def get_mini_sudoku_board(self, main_div_class):
        board = {}

        div = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, main_div_class))
        )
        div_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(div_content, 'html.parser')
        mini_sudoku_div = soup.find('div', class_=main_div_class)
        board['size'] = self.get_board_size(mini_sudoku_div)[0]
        board.update(self.parse_board_content(mini_sudoku_div, board['size']))

        return board

    @staticmethod
    def get_board_size(board_div):
        style = board_div.get('style')
        rows = int(re.search(r'--rows: (\d+);', style).group(1))
        cols = int(re.search(r'--cols: (\d+)', style).group(1))
        return rows, cols


    @staticmethod
    def parse_board_content(board_div, size):
        board = {'hints': [[0 for _ in range(size)] for _ in range(size)]}
        cells = board_div.find_all("div", class_="sudoku-cell-content")
        idx = 0
        for cell in cells:
            if cell.get_text() != '\n':
                j, i = idx % size, idx // size
                board['hints'][i][j] = int(cell.get_text())
            idx += 1
        return board
