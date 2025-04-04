from z3 import *
from collections import defaultdict


class QueensEncoding:
    def __init__(self, board, size):
        self.board = board
        self.size = size
        self.diagonal_pos = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

    def queens_variable(self):
        n_bits = math.ceil(math.log2(self.size))
        return [BitVec(f'{i}', n_bits) for i in range(self.size)]

    def color_region_variables(self):
        # A single boolean variable is referenced in two data structures for color region constraints
        color_region = defaultdict(list)
        painted_cells = {}
        for i in range(self.size):
            for j in range(self.size):
                var = BitVec(f'is_{i}_{j}_painted', 1)
                painted_cells[(i, j)] = var
                color_region[self.board[i][j]].append(var)

        return color_region, painted_cells

    def queens_domain_constraint(self, queens):
        return [And(UGE(queens[i], 0), ULE(queens[i], self.size-1)) for i in range(self.size)]

    def distinct_rows_constraint(self, queens):
        return [Distinct(queens)]

    def free_diagonals_constraint(self, painted_cells):
        c = []
        for i in range(self.size):
            for j in range(self.size):
                not_painted = []
                for pos in self.diagonal_pos:
                    x, y = i + pos[0], j + pos[1]
                    if 0 <= x < self.size and 0 <= y < self.size:
                        not_painted.append(painted_cells[(x, y)] == 0)
                c.append(Implies(painted_cells[(i, j)] == 1, And(not_painted)))

        return c

    def one_queen_per_color_constraint(self, queens, color_region, painted_cells):
        c1 = [If(queens[i] == j, painted_cells[(j, i)] == 1, painted_cells[(j, i)] == 0)
              for i in range(self.size)
              for j in range(self.size)]
        c2 = [Sum([If(pos == 1, 1, 0) for pos in region]) == 1 for region in color_region.values()]

        return c1 + c2
