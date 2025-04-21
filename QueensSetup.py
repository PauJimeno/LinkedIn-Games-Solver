from src.solver.QueensSolver import QueensSolver
from src.scraper.QueensScraper import QueensScraper
from src.visualizer.QueensPrinter import QueensPrinter
from src.base.BaseSetup import BaseSetup
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    queens_setup = QueensSetup()
    queens_instance = queens_setup.fetch_game_data()
    queens_solver = QueensSolver(queens_instance['board'], queens_instance['rows'])
    queens_setup.set_solver(queens_solver)
    solution = queens_setup.solve_instance(queens_instance)

    if solution:
        queens_printer = QueensPrinter(
            queens_instance['board'], queens_instance['rows'], solution, queens_setup.styles['color_palette'])
        queens_printer.solution_to_terminal()
        queens_printer.solution_as_image(f"{queens_setup.board_folder}/board_{queens_instance['number']}.png")


class QueensSetup(BaseSetup):
    def __init__(self):
        super().__init__('queens')
        self.scraper = QueensScraper(self.web_literals[self.game_type]['webpage_url'])

    def fetch_game_data(self):
        time_before = time.time()
        self.scraper.set_up_driver()
        board_data = {}
        try:
            self.scraper.check_iframe()
            board_data['number'] = self.scraper.get_board_number(self.web_literals['level_number_class'])
            self.scraper.access_main_page(self.web_literals['play_button_ids'])
            board_data.update(
                self.scraper.get_queens_board(
                    self.web_literals[self.game_type]['board_div_id'],
                    self.web_literals[self.game_type]['board_div_class'])
            )
        finally:
            self.scraper.close_web_driver()

        fetching_time = round(time.time() - time_before, 3)
        print(f'Queens Board data fetched in {fetching_time}s')

        return board_data


if __name__ == '__main__':
    main()
