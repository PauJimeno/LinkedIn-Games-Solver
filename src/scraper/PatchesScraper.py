from scraper.Scraper import Scraper

from collections import defaultdict
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class PatchesScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def get_patches_board(self, main_div_class):
        board = {}

        div = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, main_div_class))
        )
        div_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(div_content, 'html.parser')
        patches_div = soup.find('div', attrs={'data-testid': 'interactive-grid'})

        board['size'] = self.get_board_size(patches_div)[0]
        board.update(self.parse_board_content(patches_div))

        return board

    @staticmethod
    def get_board_size(board_div):
        style = board_div.get('style', '')
        values = [int(x) for x in re.findall(r':\s*(\d+)', style)]
        rows = values[0]
        cols = values[1]

        return rows, cols

    @staticmethod
    def parse_board_content(board_div):
        board = {"hints": {}, 'colours': {}}
        cells = board_div.find_all("div", {"data-shape": True})
        for cell in cells:
            idx = int(cell.parent.parent.get("data-cell-idx"))
            hint_type = cell.get("data-shape").replace("PatchesShapeConstraint_","")
            board["hints"].update({idx:[hint_type]})
            size_span = cell.parent.find("span", attrs={"data-testid": True})
            hex_colour = re.findall(r':\s*#([A-Za-z0-9]{6})', cell.parent.parent.get('style', ''))[0]
            board['colours'].update({idx: hex_colour})
            if size_span is not None:
                hint_size = int(size_span.get_text())
                board["hints"][idx].append(hint_size)

        return board
