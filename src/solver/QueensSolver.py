from src.solver.Encoding import Encoding
import time
from z3 import *


class QueensSolver:
    def __init__(self, board, size):
        self.board = board
        self.size = size
        self.encoding = Encoding(self.board, self.size)
        self.computing_time = 0

        # Solver definition
        self.solver = Solver()

        # Variable definition
        self.queens = self.encoding.queens_variable()
        self.color_region, self.painted_cells = self.encoding.color_region_variables()

        # Constraint loading
        self.solver.add(
            self.encoding.queens_domain_constraint(self.queens) +
            self.encoding.distinct_rows_constraint(self.queens) +
            self.encoding.free_diagonals_constraint(self.painted_cells) +
            self.encoding.one_queen_per_color_constraint(self.queens, self.color_region, self.painted_cells)
        )

    def solve_board(self):
        time_before = time.time()
        has_solution = self.solver.check() == sat
        self.computing_time = round(time.time() - time_before, 3)

        return has_solution

    def get_model(self):
        return [int(str(self.solver.model()[queen])) for queen in self.queens]
