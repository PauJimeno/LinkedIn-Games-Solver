# -*- coding: utf-8 -*-

class ZipPrinter:
    def __init__(self, solution, waypoints, size, charset, background):
        self.solution = solution
        self.waypoints = waypoints
        self.size = size
        self.charset = charset
        self.background = background
        self.dir_map = {
            (0, -1): 0,
            (1, 0): 1,
            (0, 1): 2,
            (-1, 0): 3
        }
        self.path_map = {
            (0, 1): [' ┗━', ' ╚═', ' └─'],
            (1, 0): [' ┗━', ' ╚═', ' └─'],
            (0, 2): [' ┃ ', ' ║ ', ' │ '],
            (2, 0): [' ┃ ', ' ║ ', ' │ '],
            (0, 3): ['━┛ ', '═╝ ', '─┘ '],
            (3, 0): ['━┛ ', '═╝ ', '─┘ '],
            (1, 2): [' ┏━', ' ╔═', ' ┌─'],
            (2, 1): [' ┏━', ' ╔═', ' ┌─'],
            (1, 3): ['━━━', '═══', '───'],
            (3, 1): ['━━━', '═══', '───'],
            (2, 3): ['━┓ ', '═╗ ', '─┐ '],
            (3, 2): ['━┓ ', '═╗ ', '─┐ ']
        }

    def get_path_char(self, x, y, value, index):
        cell_bef, cell_aft = 0, 0
        cell_idx = y * self.size + x
        if cell_idx in self.waypoints:
            char = f'{str(self.waypoints.index(cell_idx)+1).rjust(2)} '
        else:
            for direction in self.dir_map.keys():
                xi, yi = x + direction[0], y + direction[1]
                if 0 <= xi < self.size and 0 <= yi < self.size:
                    neigh_cell = self.solution[yi][xi]
                    if neigh_cell == value - 1:
                        cell_bef = self.dir_map[(direction[0], direction[1])]
                    elif neigh_cell == value + 1:
                        cell_aft = self.dir_map[(direction[0], direction[1])]
            char = self.path_map[(cell_bef, cell_aft)][index]

        return char

    def solution_to_terminal(self):
        alternator = 0
        cell = '\u001B[48;2;{};{};{}m\u001B[38;2;0;0;0m{}\u001B[0m'
        for i in range(self.size):
            for j in range(self.size):
                char = self.get_path_char(j, i, self.solution[i][j], self.charset)
                r, g, b = self.background[alternator][0], self.background[alternator][1], self.background[alternator][2]
                print(cell.format(r, g, b, char), end='')
                alternator = not alternator
            if self.size % 2 == 0:
                alternator = not alternator
            print()


