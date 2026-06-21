from z3 import *


class MiniSudokuEncoding:
    def __init__(self, size, hints):
        self.size = size
        self.hints = hints

    def cell_variable(self):
        n_bits = math.ceil(math.log2(self.size))
        return [[BitVec(f'C_{j}_{i}', n_bits) for i in range(self.size)] for j in range(self.size)]

    def cell_domain(self, cells):
        return [And(UGE(cells[i][j], 1), ULE(cells[i][j], self.size)) for i in range(self.size) for j in range(self.size)]

    def force_hint(self, cells):
        constraint = []
        for i in range(self.size):
            for j in range(self.size):
                if self.hints[i][j] != 0:
                    constraint.append(cells[i][j]==self.hints[i][j])
        return constraint

    def row_col_alldiff(self, cells):
        constraint = []
        for i in range(self.size):
            constraint.append(Distinct(cells[i]))
            constraint.append(Distinct([cells[j][i] for j in range(self.size)]))
        return constraint

    def group_alldiff(self, cells):
        constraint = []
        for ii in range(0, self.size, 2): # Row subgroups (0, 2, 4)
            for jj in range(0, self.size, 3): # Column subgroups (0, 3)
                group_cells = []
                for i in range(self.size//3):
                    for j in range(self.size//2):
                        group_cells.append(cells[ii+i][jj+j])
                constraint.append(Distinct(group_cells))
        return constraint
