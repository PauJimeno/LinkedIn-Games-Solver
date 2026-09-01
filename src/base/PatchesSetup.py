from solver.PatchesSolver import PatchesSolver
from scraper.PatchesScraper import PatchesScraper
from visualizer.PatchesPrinter import PatchesPrinter
from base.BaseSetup import BaseSetup
from datetime import date
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    patches_setup = PatchesSetup()
    patches_instance = patches_setup.fetch_game_data()
    patches_solver = PatchesSolver(patches_instance['size'], patches_instance['hints'])
    patches_setup.set_solver(patches_solver)
    solution = patches_setup.solve_instance(patches_instance)

    if solution:
        patches_printer = PatchesPrinter(
            solution, patches_instance['size'], patches_instance['hints'], patches_instance['colours'])
        patches_printer.solution_to_terminal()


class PatchesSetup(BaseSetup):
    def __init__(self):
        super().__init__('patches')
        self.scraper = PatchesScraper(self.web_literals[self.game_type]['webpage_url'])

    def fetch_game_data(self):
        board_data = {}
        time_before = time.time()
        self.scraper.set_up_driver()
        try:
            self.scraper.check_iframe()
            board_data['number'] = date.today().strftime('%d-%m-%Y')
            self.scraper.access_main_page(self.web_literals[self.game_type]['play_button'])
            board_data.update(self.scraper.get_patches_board(self.web_literals[self.game_type]['board_div_class']))
        finally:
            self.scraper.close_web_driver()

        fetching_time = round(time.time() - time_before, 3)
        print(f'Patches board data fetched in {fetching_time}s')

        return board_data


if __name__ == '__main__':
    main()
