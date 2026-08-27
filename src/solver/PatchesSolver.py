from solver.GenericSolver import GenericSolver
from solver.PatchesEncoding import PatchesEncoding


class PatchesSolver(GenericSolver):
    def __init__(self, size, hints):
        super().__init__()
        self.size = size
        self.hints = hints
        self.encoding = PatchesEncoding(self.size, hints)

        self.corners = self.encoding.corners_variable()
        self.solver.add(
            self.encoding.cell_domain(self.corners) +
            self.encoding.relative_pos(self.corners) +
            self.encoding.area_shape(self.corners) +
            self.encoding.area_size(self.corners) +
            self.encoding.area_overlap(self.corners) +
            self.encoding.fill_board(self.corners)
        )

    def get_model(self):
        solution = [[0 for _ in range(0, self.size)] for _ in range(0, self.size)]
        for idx, data in self.corners.items():
            var_x1, var_y1 = data['pos'][0]
            var_x2, var_y2 = data['pos'][1]
            x1 = int(str(self.solver.model()[var_x1]))
            y1 = int(str(self.solver.model()[var_y1]))
            x2 = int(str(self.solver.model()[var_x2]))
            y2 = int(str(self.solver.model()[var_y2]))
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    solution[j][i] = idx

        return solution
