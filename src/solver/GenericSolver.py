import time
from z3 import *


class GenericSolver:
    def __init__(self):
        # Solving time
        self.computing_time = 0

        # Solver definition
        self.solver = Solver()

    def solve_puzzle(self):
        time_before = time.time()
        has_solution = self.solver.check() == sat
        self.computing_time = round(time.time() - time_before, 3)

        return has_solution

    def get_model(self):
        raise 'get_model() method must be implemented'
