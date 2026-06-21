from solver.GenericSolver import GenericSolver
from solver.MiniSudokuEncoding import MiniSudokuEncoding
from z3 import is_true


class MiniSudokuSolver(GenericSolver):
    def __init__(self, size, hints):
        super().__init__()
        self.size = size
        self.encoding = MiniSudokuEncoding(self.size, hints)

        self.cells = self.encoding.cell_variable()
        self.solver.add(
            self.encoding.cell_domain(self.cells) +
            self.encoding.force_hint(self.cells) +
            self.encoding.row_col_alldiff(self.cells) +
            self.encoding.group_alldiff(self.cells)
        )

    def get_model(self):
        return [[int(str(self.solver.model()[self.cells[j][i]])) for i in range(self.size)] for j in range(self.size)]
