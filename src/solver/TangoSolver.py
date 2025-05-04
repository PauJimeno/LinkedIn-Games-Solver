from solver.GenericSolver import GenericSolver
from solver.TangoEncoding import TangoEncoding
from z3 import is_true


class TangoSolver(GenericSolver):
    def __init__(self, size, hints_1, hints_2):
        super().__init__()
        self.size = size
        self.encoding = TangoEncoding(self.size, hints_1, hints_2)

        self.element = self.encoding.element_variable()
        self.solver.add(
            self.encoding.at_most_two_column(self.element) +
            self.encoding.at_most_two_row(self.element) +
            self.encoding.equal_column(self.element) +
            self.encoding.equal_row(self.element) +
            self.encoding.hint_placement(self.element) +
            self.encoding.opp_eq_hint(self.element)
        )

    def get_model(self):
        return [[1 if is_true(self.solver.model()[self.element[i][j]]) else 0 for i in range(self.size)] for j in range(self.size)]
