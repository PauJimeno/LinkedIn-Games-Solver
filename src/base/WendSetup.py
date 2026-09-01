from solver.WendSolver import WendSolver
from scraper.WendScraper import WendScraper
from visualizer.WendPrinter import WendPrinter
from base.BaseSetup import BaseSetup
from datetime import date
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    wend_setup = WendSetup()
    wend_instance = wend_setup.fetch_game_data()
    wend_solver = WendSolver(wend_instance['size'], wend_instance['board'], wend_instance['words'])
    wend_setup.set_solver(wend_solver)
    solution = wend_setup.solve_instance(wend_instance)

    if solution:
        wend_printer = WendPrinter(
            solution['board'], solution['words'], wend_instance['size'], wend_instance['board'], wend_setup.styles['color_palette'])
        wend_printer.solution_to_terminal()


class WendSetup(BaseSetup):
    def __init__(self):
        super().__init__('wend')
        self.scraper = WendScraper(self.web_literals[self.game_type]['webpage_url'])

    def fetch_game_data(self):
        board_data = {}
        time_before = time.time()
        self.scraper.set_up_driver()
        try:
            self.scraper.check_iframe()
            board_data['number'] = date.today().strftime('%d-%m-%Y')
            self.scraper.access_main_page(self.web_literals[self.game_type]['play_button'])
            board_data.update(self.scraper.get_wend_board(self.web_literals[self.game_type]['board_div_class']))
        finally:
            self.scraper.close_web_driver()

        fetching_time = round(time.time() - time_before, 3)
        print(f'Wend board data fetched in {fetching_time}s')

        return board_data


if __name__ == '__main__':
    main()
