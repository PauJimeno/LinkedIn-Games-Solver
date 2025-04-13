from src.solver.ZipSolver import ZipSolver
from src.board_scrapper.ZipScrapper import ZipScrapper
from pprint import pprint
import json
import time

SOLVED_BOARDS = 'resources/solved_boards/Zip'
BOARD_INSTANCES = 'resources/instances/Zip'
GAME = 'zip'

INSTANCE_15 = {
    'walls': {
        0: ['DOWN'],
        3: ['DOWN'],
        5: ['DOWN'],
        6: ['DOWN'],
        8: ['DOWN'],
        10: ['RIGHT'],
        12: ['DOWN'],
        15: ['RIGHT'],
        17: ['DOWN', 'RIGHT'],
        19: ['RIGHT'],
        22: ['RIGHT'],
        23: ['RIGHT'],
        26: ['DOWN', 'RIGHT'],
        29: ['RIGHT'],
        30: ['RIGHT'],
        31: ['DOWN'],
        33: ['RIGHT'],
        36: ['DOWN', 'RIGHT'],
        37: ['DOWN'],
        40: ['DOWN', 'RIGHT']
    },
    'ordered_sequence': [0, 3, 6],
    'size': 7
}


def load_literals():
    with open('resources/variables/html_literals.json') as f:
        web_literals = json.load(f)
    return web_literals


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


web_literals = load_literals()
instance = fetch_game_data(web_literals)
solution = solve_instance(instance)

if solution:
    pprint(solution)
    instance['solution'] = solution
    save_json(instance, f"{BOARD_INSTANCES}/instance_{instance['number']}")
