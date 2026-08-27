from z3 import *


class PatchesEncoding:
    def __init__(self, size, hints):
        self.size = size
        self.hints = hints

    def corners_variable(self):
        corners = {}
        n_bits = math.ceil(math.log2(self.size*self.size))
        for idx, hint in self.hints.items():
            pos_1 = (BitVec(f'X_{idx}_1', n_bits), BitVec(f'Y_{idx}_1', n_bits))
            pos_2 = (BitVec(f'X_{idx}_2', n_bits), BitVec(f'Y_{idx}_2', n_bits))
            corners[idx] = {"hint": hint, "pos": [pos_1, pos_2]}

        return corners

    def cell_domain(self, corners):
        domain = []
        for idx, data in corners.items():
            x1, x2 = data['pos'][0]
            y1, y2 = data['pos'][1]
            domain.append(And(ULT(x2, self.size), ULT(y2, self.size))) # Bottom right corner is within bounds
            domain.append(And(ULT(x1, self.size), ULT(y1, self.size)))
        return domain

    def relative_pos(self, corners):
        pos_constraint = []
        for idx, data in corners.items():
            x1, y1 = data['pos'][0]
            x2, y2 = data['pos'][1]
            x, y = idx % self.size, idx // self.size
            pos_constraint.append(And(ULE(x1, x), ULE(y1, y))) # Top left corner is correct relative to hint center
            pos_constraint.append(And(UGE(x2, x), UGE(y2, y))) # Bottom right corner is correct relative to hint center

            pos_constraint.append(And(ULE(x1, x2), ULE(y1, y2))) # x1 is to the left of x2, y2 is bellow y1

        return pos_constraint

    @staticmethod
    def area_shape(corners):
        shape_constraint = []
        for idx, data in corners.items():
            x1, y1 = data['pos'][0]
            x2, y2 = data['pos'][1]
            hint_shape = data['hint'][0] # Extract hint shape (VERTICAL_RECT, HORIZONTAL_RECT, SQUARE or UNKNOWN)
            if hint_shape == 'SQUARE':
                shape_constraint.append(x2-x1 == y2-y1)  # Both sides have the same length
            elif hint_shape == 'VERTICAL_RECT':
                shape_constraint.append(UGT(y2-y1, x2-x1)) # Strictly taller than wider
            elif hint_shape == 'HORIZONTAL_RECT':
                shape_constraint.append(ULT(y2 - y1, x2 - x1)) # Strictly wider than taller

        return shape_constraint

    @staticmethod
    def area_size(corners):
        size_constraint = []
        for idx, data in corners.items():
            x1, y1 = data['pos'][0]
            x2, y2 = data['pos'][1]
            if len(data['hint']) == 2: # Hint contains size
                size = data['hint'][1]
                size_constraint.append((x2-x1+1)*(y2-y1+1)==size)

        return size_constraint

    def area_overlap(self, corners):
        overlap_constraint = []

        indices = list(corners.keys())

        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                idx1 = indices[i]
                idx2 = indices[j]

                x1, y1 = corners[idx1]['pos'][0]
                x2, y2 = corners[idx1]['pos'][1]

                x3, y3 = corners[idx2]['pos'][0]
                x4, y4 = corners[idx2]['pos'][1]

                overlap_constraint.append(
                    Or(
                        ULT(x2, x3),  # R1 is left of R2
                        ULT(x4, x1),  # R2 is left of R1
                        ULT(y4, y1),  # R1 is above R2
                        ULT(y2, y3)  # R2 is above R1
                    )
                )

        return overlap_constraint

    def fill_board(self, corners):
        areas = []
        for idx, data in corners.items():
            x1, y1 = data['pos'][0]
            x2, y2 = data['pos'][1]
            areas.append((x2-x1+1)*(y2-y1+1))
        return [Sum(areas)==self.size*self.size]