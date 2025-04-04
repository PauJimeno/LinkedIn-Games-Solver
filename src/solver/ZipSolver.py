from src.solver.GenericSolver import GenericSolver
from src.solver.ZipEncoding import ZipEncoding


class ZipSolver(GenericSolver):
    def __init__(self, walls, waypoints, size):
        super().__init__()
        self.walls = walls
        self.waypoints = waypoints
        self.size = size
        self.encoding = ZipEncoding(self.walls, self.waypoints, self.size)

        self.path = self.encoding.path_variable()
        self.solver.add(
            self.encoding.path_domain_constraint(self.path) +
            self.encoding.path_propagation_constraint(self.path) +
            self.encoding.waypoint_sequence_constraint(self.path)
        )

        self.encoding.add_wall_redundancy()

    def get_model(self):
        return [[int(str(self.solver.model()[self.path[i][j]])) for i in range(self.size)] for j in range(self.size)]
