import json
import click


class BaseSetup:
    STYLES = 'resources/variables/styles.json'
    INSTANCES = 'resources/instances'
    BOARDS = 'resources/solved_boards'
    WEB_LITERALS = 'resources/variables/html_literals.json'

    def __init__(self, game_type):
        self.game_type = game_type
        self.printer = None
        self.solver = None
        self.web_literals = self.load_json(BaseSetup.WEB_LITERALS)
        self.styles = self.load_json(BaseSetup.STYLES)[self.game_type]
        self.save_folder = f"{BaseSetup.INSTANCES}/{self.game_type}"
        self.board_folder = f"{BaseSetup.BOARDS}/{self.game_type}"

    def set_solver(self, solver):
        self.solver = solver

    def set_visualizer(self, printer):
        self.printer = printer

    def solve_instance(self, instance):
        solution = []
        if self.solver.solve_puzzle():
            print(f"{self.game_type} Puzzle #{instance['number']} solved in {self.solver.computing_time}s")
            solution = self.solver.get_model()
            instance['solution'] = solution
            self.save_json(instance, f"{self.save_folder}/instance_{instance['number']}")
        else:
            print(f"{self.game_type} Puzzle #{instance['number']} has no solution")

        return solution

    def print_solution(self):
        self.printer.solution_to_terminal()

    @staticmethod
    def load_json(path):
        with open(path) as f:
            json_content = json.load(f)
        return json_content

    @staticmethod
    def save_json(data, path):
        with open(f"{path}.json", 'w') as f:
            json.dump(data, f)
