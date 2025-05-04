from z3 import *


class TangoEncoding:
    def __init__(self, size, hints_1, hints_2):
        self.size = size
        self.hints_1 = hints_1
        self.hints_2 = hints_2
        self.adjacent_pos = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }

    def element_variable(self):
        return [[Bool(f"E_{i}_{j}") for i in range(self.size)] for j in range(self.size)]

    def equal_row(self, element):
        constraint = []
        for i in range(self.size):
            constraint.append(Sum([If(element[i][j], 1, 0) for j in range(self.size)]) == self.size/2)

        return constraint

    def equal_column(self, element):
        constraint = []
        for j in range(self.size):
            constraint.append(Sum([If(element[i][j], 1, 0) for i in range(self.size)]) == self.size/2)

        return constraint

    def at_most_two_row(self, element):
        constraint = []
        for i in range(self.size):
            for j in range(self.size-2):
                a, b, c = element[i][j], element[i][j+1], element[i][j+2]
                constraint.append(And(Not(And(a,b,c)), Or(a,b,c)))

        return constraint

    def at_most_two_column(self, element):
        constraint = []
        for j in range(self.size):
            for i in range(self.size-2):
                a, b, c = element[i][j], element[i+1][j], element[i+2][j]
                constraint.append(And(Not(And(a,b,c)), Or(a,b,c)))

        return constraint

    def hint_placement(self, element):
        constraint = []

        suns = self.hints_1[0]
        moons = self.hints_1[1]

        for moon in moons:
            i, j = moon % self.size, moon // self.size
            constraint.append(element[i][j])

        for sun in suns:
            i, j = sun % self.size, sun // self.size
            constraint.append(Not(element[i][j]))

        return constraint

    def opp_eq_hint(self, element):
        constraint = []
        for index, directions in self.hints_2['equal'].items():
            x, y = index % self.size, index // self.size
            for direction in directions:
                xi, yi = x + self.adjacent_pos[direction][0], y + self.adjacent_pos[direction][1]
                a, b = element[x][y], element[xi][yi]
                constraint.append(Or(Not(Or(a,b)), And(a, b)))

        for index, directions in self.hints_2['diff'].items():
            x, y = index % self.size, index // self.size
            for direction in directions:
                xi, yi = x + self.adjacent_pos[direction][0], y + self.adjacent_pos[direction][1]
                constraint.append(Xor(element[x][y], element[xi][yi]))

        return constraint

