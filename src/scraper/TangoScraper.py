from scraper.Scraper import Scraper

from collections import defaultdict
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class TangoScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def get_tango_board(self, main_div_class):
        board = {}

        div = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, main_div_class))
        )
        div_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(div_content, 'html.parser')
        tango_div = soup.find('div', class_=main_div_class)
        board['size'] = self.get_board_size(tango_div)[0]
        board.update(self.parse_board_content(tango_div))

        return board

    @staticmethod
    def get_board_size(board_div):
        style = board_div.get('style')
        rows = int(re.search(r'--rows: (\d+);', style).group(1))
        cols = int(re.search(r'--cols: (\d+)', style).group(1))
        return rows, cols


    @staticmethod
    def parse_board_content(board_div):
        pattern = re.compile(r"^lotka-cell-edge--")
        board = {'hints_1': [[],[]], 'hints_2': {'equal':defaultdict(list), 'diff':defaultdict(list)}}
        cells = board_div.find_all("div", class_="lotka-cell")
        for cell in cells:
            cell_idx = int(cell.get("data-cell-idx"))
            if cell.find_all("g", id="Moon"):
                board['hints_1'][1].append(cell_idx)
            if cell.find_all("g", id="Sun"):
                board['hints_1'][0].append(cell_idx)
            adjacent_hints = cell.find_all("div", class_=pattern)
            for adjacent_hint in adjacent_hints:
                pos = re.search(r'--(\w+)', adjacent_hint.attrs['class'][1]).group(1)
                if adjacent_hint.find("svg", attrs={"aria-label": "Equal"}):
                    board['hints_2']['equal'][cell_idx].append(pos.upper())
                if adjacent_hint.find("svg", attrs={"aria-label": "Cross"}):
                    board['hints_2']['diff'][cell_idx].append(pos.upper())

        return board
