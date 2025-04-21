from solver.QueensEncoding import QueensEncoding
from solver.GenericSolver import GenericSolver


class QueensSolver(GenericSolver):
    def __init__(self, board, size):
        super().__init__()
        self.board = board
        self.size = size
        self.encoding = QueensEncoding(self.board, self.size)

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

    def get_model(self):
        return [int(str(self.solver.model()[queen])) for queen in self.queens]
