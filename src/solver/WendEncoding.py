from z3 import *


class WendEncoding:
    def __init__(self, size, board, words):
        self.size = size
        self.board = board
        self.words = words
        self.total_letters = sum(words)
        self.total_words = len(words)
        self.domain = self.total_letters + self.total_words + 1
        self.end = self.word_end()
        self.start = self.word_start()
        self.mid = self.word_mid()
        self.adjacent_cells = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def neighbours(self, i, j):
        neigh = []
        for x, y in self.adjacent_cells:
            rel_x = x + j
            rel_y = y + i
            if 0 <= rel_x < self.size and 0 <= rel_y < self.size and self.board[rel_y][rel_x]:
                neigh.append((rel_y, rel_x))
        return neigh

    def word_start(self):
        start_val = []
        count = 0
        for word in self.words:
            start_val.append(count)
            count += word + 1
        return start_val

    def word_mid(self):
        mid_val = []
        count = 0
        for word in self.words:
            if word>2:
                for i in range(1, word-1):
                    mid_val.append(i+count)
            count += word + 1
        return mid_val

    def word_end(self):
        end_val = []
        count = -1
        for word in self.words:
            count += word
            end_val.append(count)
            count += 1

        return end_val

    def outside_word(self):
        end_val = []
        count = -1
        for word in self.words:
            count += word
            end_val.append(count+1)
            count += 1

        return end_val

    def word_layout_variable(self):
        n_bits = math.ceil(math.log2(self.domain))
        return [[BitVec(f'L_{j}_{i}', n_bits) for i in range(self.size)] for j in range(self.size)]

    def word_domain(self, word_layout):
        domain = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]: # Position i j has a letter
                    domain.append(ULT(word_layout[i][j], self.domain - 2)) # All except last value of domain are valid
                    domain.append(Distinct(word_layout[i][j], *self.outside_word()))
                else: # Position i j has no letter "blocked cell"
                    domain.append(word_layout[i][j]==self.domain-1) # Only the last value of the domain is valid
        return domain

    def unique_word_constraint(self, word_layout):
        usable_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    usable_cells.append(word_layout[i][j])
        return [Distinct(usable_cells)]


    def word_structure(self, word_layout):
        constraint = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    pred, succ = [], []
                    for y, x in self.neighbours(i, j):
                        pred.append(If(word_layout[i][j] == word_layout[y][x] + 1, 1, 0))
                        succ.append(If(word_layout[i][j] == word_layout[y][x] - 1, 1, 0))
                    for start_idx in self.start:
                        constraint.append(Implies(word_layout[i][j] == start_idx, Sum(succ) == 1))
                        constraint.append(Implies(word_layout[i][j] == start_idx, Sum(pred) == 0))
                    for end_idx in self.end:
                        constraint.append(Implies(word_layout[i][j] == end_idx, Sum(succ) == 0))
                        constraint.append(Implies(word_layout[i][j] == end_idx, Sum(pred) == 1))
                    for mid_idx in self.mid:
                        constraint.append(Implies(word_layout[i][j] == mid_idx, Sum(succ) == 1))
                        constraint.append(Implies(word_layout[i][j] == mid_idx, Sum(pred) == 1))

        return constraint
