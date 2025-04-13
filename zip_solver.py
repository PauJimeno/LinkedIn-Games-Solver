from src.solver.ZipSolver import ZipSolver
from src.board_scrapper.ZipScrapper import ZipScrapper
from src.visualizer.ZipPrinter import ZipPrinter
import json
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

SOLVED_BOARDS = 'resources/solved_boards/Zip'
BOARD_INSTANCES = 'resources/instances/Zip'
STYLES = 'resources/variables/styles.json'
WEB_LITERALS = 'resources/variables/html_literals.json'
GAME = 'zip'


def load_json(path):
    with open(path) as f:
        json_content = json.load(f)
    return json_content


def fetch_game_data(web_literals):
    time_before = time.time()

    game_scrapper = ZipScrapper(web_literals[GAME]['webpage_url'])
    game_scrapper.set_up_driver()
    board_data = {}
    try:
        game_scrapper.check_iframe()
        board_data['number'] = game_scrapper.get_board_number(web_literals['level_number_class'])
        game_scrapper.access_main_page(web_literals['play_button_ids'])
        board_data.update(game_scrapper.get_zip_board(web_literals[GAME]['board_div_class']))
    finally:
        game_scrapper.close_web_driver()

    fetching_time = round(time.time() - time_before, 3)
    print(f'Zip Board data fetched in {fetching_time}s')

    return board_data


def solve_instance(instance):
    zip_solver = ZipSolver(instance['walls'], instance['ordered_sequence'], instance['size'])
    solution = []
    if zip_solver.solve_puzzle():
        print(f"Zip Puzzle #{instance['number']} solved in {zip_solver.computing_time}s")
        solution = zip_solver.get_model()
    else:
        print(f"Zip Puzzle #{instance['number']} has no solution")

    return solution


def save_json(data, path):
    with open(f"{path}.json", 'w') as f:
        json.dump(data, f)


web_literals = load_json(WEB_LITERALS)
styles = load_json(STYLES)
instance = fetch_game_data(web_literals)
solution = solve_instance(instance)

if solution:
    instance['solution'] = solution
    visualizer = ZipPrinter(
        instance['solution'], instance['ordered_sequence'],
        instance['size'], styles[GAME]['line_style'], styles[GAME]['background'])
    visualizer.solution_to_terminal()
    save_json(instance, f"{BOARD_INSTANCES}/instance_{instance['number']}")
