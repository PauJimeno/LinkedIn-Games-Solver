from solver.ZipSolver import ZipSolver
from scraper.ZipScraper import ZipScraper
from visualizer.ZipPrinter import ZipPrinter
from base.BaseSetup import BaseSetup
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    zip_setup = ZipSetup()
    zip_instance = zip_setup.fetch_game_data()
    zip_solver = ZipSolver(zip_instance['walls'], zip_instance['ordered_sequence'], zip_instance['size'])
    zip_setup.set_solver(zip_solver)
    solution = zip_setup.solve_instance(zip_instance)

    if solution:
        zip_printer = ZipPrinter(
            solution, zip_instance['ordered_sequence'], zip_instance['size'], 1, zip_setup.styles['background'])
        zip_printer.solution_to_terminal()


class ZipSetup(BaseSetup):
    def __init__(self):
        super().__init__('zip')
        self.scraper = ZipScraper(self.web_literals[self.game_type]['webpage_url'])

    def fetch_game_data(self):
        board_data = {}
        time_before = time.time()
        self.scraper.set_up_driver()
        try:
            self.scraper.check_iframe()
            board_data['number'] = self.scraper.get_board_number(self.web_literals['level_number_class'])
            self.scraper.access_main_page(self.web_literals['play_button_ids'])
            board_data.update(self.scraper.get_zip_board(self.web_literals[self.game_type]['board_div_class']))
        finally:
            self.scraper.close_web_driver()

        fetching_time = round(time.time() - time_before, 3)
        print(f'Zip Board data fetched in {fetching_time}s')

        return board_data


if __name__ == '__main__':
    main()
