from collections import defaultdict
from z3 import *


class ZipEncoding:
    def __init__(self, walls, waypoints, size):
        self.walls = defaultdict(list)
        self.walls.update(walls)
        self.waypoints = waypoints
        self.size = size
        self.adjacent_pos = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        self.opposite_dir = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }

        self.add_wall_redundancy()

    def path_variable(self):
        n_bits = math.ceil(math.log2(self.size*self.size))
        return [[BitVec(f"R_{i}_{j}", n_bits) for i in range(self.size)] for j in range(self.size)]

    def path_domain_constraint(self, path):
        # Each variable can take value from [0..width*height-1], 0 lower bound implicit from BitVec variable
        return [ULT(path[i][j], self.size*self.size) for i in range(self.size) for j in range(self.size)]

    def path_propagation_constraint(self, path):
        constraint = []
        for i in range(self.size):
            for j in range(self.size):
                if not self.is_path_begin(i, j) and not self.is_path_end(i, j):
                    neigh_cells = []
                    for x, y in self.neighbouring_cells(i, j):
                        neigh_cells.append(path[x][y])
                    current_cell = path[i][j]
                    constraint.append(Sum([If(cell == current_cell + 1, 1, 0) for cell in neigh_cells]) == 1)
                    constraint.append(Sum([If(cell == current_cell - 1, 1, 0) for cell in neigh_cells]) == 1)

        return constraint

    def waypoint_sequence_constraint(self, path):
        constraint = []
        for i in range(len(self.waypoints) - 1):
            x, y = self.waypoints[i] % self.size, self.waypoints[i] // self.size
            x1, y1 = self.waypoints[i+1] % self.size, self.waypoints[i+1] // self.size
            constraint.append(ULT(path[x][y], path[x1][y1]))

        return constraint

    def path_start_end_constraint(self, path):
        constraint = []
        i1, j1 = self.path_begin()
        i2, j2 = self.path_end()

        constraint.append(And(path[i1][j1] == 0, path[i2][j2] == self.size*self.size - 1))

        return constraint

    def neighbouring_cells(self, x, y):
        # Given an (x, y) coordinate returns a list of accessible neighbouring cell positions
        neighbour_cells = []
        cell_index = y * self.size + x
        cell_walls = self.walls.get(cell_index, [])
        possible_neigh_dir = copy.deepcopy(self.adjacent_pos)

        # Delete directions blocked by walls
        for wall_dir in cell_walls:
            possible_neigh_dir.pop(wall_dir)

        # Calculate accessible cells
        for direction in possible_neigh_dir.values():
            xi, yi = x + direction[0], y + direction[1]
            if 0 <= xi < self.size and 0 <= yi < self.size:
                neighbour_cells.append((xi, yi))

        return neighbour_cells

    def add_wall_redundancy(self):
        # Given the original walls adds the opposite direction of wall
        for cell, walls in list(self.walls.items()):
            for wall in walls:
                x, y = cell % self.size, cell // self.size
                if wall in ('RIGHT', 'DOWN'):
                    xi, yi = x + self.adjacent_pos[wall][0], y + self.adjacent_pos[wall][1]
                    cell_index = yi * self.size + xi
                    self.walls[cell_index].append(self.opposite_dir[wall])

    def is_path_begin(self, x, y):
        x1, y1 = self.path_begin()
        return x == x1 and y == y1

    def is_path_end(self, x, y):
        x1, y1 = self.path_end()
        return x == x1 and y == y1

    def path_begin(self):
        begin_index = self.waypoints[0]
        return begin_index % self.size, begin_index // self.size

    def path_end(self):
        end_index = self.waypoints[-1]
        return end_index % self.size, end_index // self.size

