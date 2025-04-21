from scraper.Scraper import Scraper

from collections import defaultdict
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class ZipScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def get_zip_board(self, main_div_class):
        board = {}

        div = WebDriverWait(self.web_driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, main_div_class))
        )
        div_content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(div_content, 'html.parser')
        zip_div = soup.find('div', class_=main_div_class)
        board['size'] = self.get_board_size(zip_div)[0]

        board.update(self.parse_board_content(zip_div))
        return board

    @staticmethod
    def get_board_size(board_div):
        style = board_div.get('style')
        rows = int(re.search(r'--rows: (\d+);', style).group(1))
        cols = int(re.search(r'--cols: (\d+)', style).group(1))
        return rows, cols

    @staticmethod
    def parse_board_content(board_div):
        walls = defaultdict(list)
        waypoints = []

        # Find all cells in the grid.
        cells = board_div.find_all("div", class_="trail-cell")
        board_info = {}

        for cell in cells:
            # Get the cell index from the data attribute, if needed.
            cell_idx = int(cell.get("data-cell-idx"))

            # Check on any inner wall elements.
            wall_elements = cell.find_all("div", class_=lambda c: c and "trail-cell-wall" in c)
            for wall in wall_elements:
                for cl in wall.get("class", []):
                    if cl.startswith("trail-cell-wall--"):
                        pos = cl.replace("trail-cell-wall--", "")
                        if pos in ['down', 'right', 'left', 'up']:
                            walls[cell_idx].append(pos.upper())

            # Check if the cell contains a trail-cell-content (i.e., a number)
            content_elem = cell.find("div", class_="trail-cell-content")
            cell_content = content_elem.get_text(strip=True) if content_elem else False

            # You can also convert the text to an integer if that makes sense.
            if cell_content and cell_content.isdigit():
                cell_content = int(cell_content)
                waypoints.append((cell_idx, cell_content))

        board_info['walls'] = walls
        board_info['ordered_sequence'] = [index for index, _ in sorted(waypoints, key=lambda x: x[1])]

        return board_info
