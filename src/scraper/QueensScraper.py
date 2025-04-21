from scraper.Scraper import Scraper

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class QueensScraper(Scraper):
    def __init__(self, queens_url):
        super().__init__(queens_url)

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
