from solver.TangoSolver import TangoSolver
from scraper.TangoScraper import TangoScraper
from visualizer.TangoPrinter import TangoPrinter
from base.BaseSetup import BaseSetup
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    tango_setup = TangoSetup()
    #tango_instance = tango_setup.load_json(f"{tango_setup.save_folder}/instance_202.json")
    tango_instance = tango_setup.fetch_game_data()
    tango_solver = TangoSolver(tango_instance['size'], tango_instance['hints_1'], tango_instance['hints_2'])
    tango_setup.set_solver(tango_solver)
    solution = tango_setup.solve_instance(tango_instance)

    if solution:
        tango_printer = TangoPrinter(solution, tango_instance['size'], tango_setup.styles['background'])
        tango_printer.solution_to_terminal()


class TangoSetup(BaseSetup):
    def __init__(self):
        super().__init__('tango')
        self.scraper = TangoScraper(self.web_literals[self.game_type]['webpage_url'])

    def fetch_game_data(self):
        board_data = {}
        time_before = time.time()
        self.scraper.set_up_driver()
        try:
            self.scraper.check_iframe()
            board_data['number'] = self.scraper.get_board_number(self.web_literals['level_number_class'])
            self.scraper.access_main_page(self.web_literals['play_button_ids'])
            board_data.update(self.scraper.get_tango_board(self.web_literals[self.game_type]['board_div_class']))
        finally:
            self.scraper.close_web_driver()

        fetching_time = round(time.time() - time_before, 3)
        print(f'Tango Board data fetched in {fetching_time}s')

        return board_data


if __name__ == '__main__':
    main()
