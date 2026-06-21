from solver.MiniSudokuSolver import MiniSudokuSolver
from scraper.MiniSudokuScraper import MiniSudokuScraper
from visualizer.MiniSudokuPrinter import MiniSudokuPrinter
from base.BaseSetup import BaseSetup
from datetime import date
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    mini_sudoku_setup = MiniSudokuSetup()
    mini_sudoku_instance = mini_sudoku_setup.fetch_game_data()
    mini_sudoku_solver = MiniSudokuSolver(mini_sudoku_instance['size'], mini_sudoku_instance['hints'])
    mini_sudoku_setup.set_solver(mini_sudoku_solver)
    solution = mini_sudoku_setup.solve_instance(mini_sudoku_instance)

    if solution:
        mini_sudoku_printer = MiniSudokuPrinter(solution, mini_sudoku_instance['size'], mini_sudoku_setup.styles['background'])
        mini_sudoku_printer.solution_to_terminal()


class MiniSudokuSetup(BaseSetup):
    def __init__(self):
        super().__init__('mini-sudoku')
        self.scraper = MiniSudokuScraper(self.web_literals[self.game_type]['webpage_url'])

    def fetch_game_data(self):
        board_data = {}
        time_before = time.time()
        self.scraper.set_up_driver()
        try:
            self.scraper.check_iframe()
            board_data['number'] = date.today().strftime('%d-%m-%Y')
            self.scraper.access_main_page(self.web_literals['play_button_ids'])
            board_data.update(self.scraper.get_mini_sudoku_board(self.web_literals[self.game_type]['board_div_class']))
        finally:
            self.scraper.close_web_driver()

        fetching_time = round(time.time() - time_before, 3)
        print(f'Mini Sudoku Board data fetched in {fetching_time}s')

        return board_data


if __name__ == '__main__':
    main()
