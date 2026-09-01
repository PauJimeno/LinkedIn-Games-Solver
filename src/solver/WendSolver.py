from z3 import UserPropagateBase
from solver.GenericSolver import GenericSolver
from solver.WendEncoding import WendEncoding
from utils.pattern_dict import PatternDict


class WendPropagator(UserPropagateBase):
    def __init__(self, s, size, domain, board_var, board, w_map, l_map, pd, ctx=None):
        super().__init__(s, ctx)
        self.size = size
        self.domain = domain
        self.board_var = board_var
        self.board = board
        self.w_map = w_map
        self.l_map = l_map
        self.pd = pd

        self.add_fixed(lambda x, v: self._fixed(x, v))

        self.assigned = {}          # id(var) -> idx (position in domain)
        self.idx_to_vid = {}        # idx -> id(var), inverse lookup for building conflicts
        self.var_of_id = {}         # id(var) -> the actual var expr (needed for conflict())
        self.var_pos = {}           # id(var) -> (i, j)
        self.current_letters = ["_"] * domain   # persistent, incrementally maintained
        self.trail = []
        self.trail_lens = []

        for i in range(size):
            for j in range(size):
                if board[i][j]:
                    v = board_var[i][j]
                    self.add(v)
                    vid = v.get_id()
                    self.var_of_id[vid] = v
                    self.var_pos[vid] = (i, j)

    def push(self):
        self.trail_lens.append(len(self.trail))

    def pop(self, n):
        for _ in range(n):
            mark = self.trail_lens.pop()
            while len(self.trail) > mark:
                vid = self.trail.pop()
                idx = self.assigned.pop(vid)
                del self.idx_to_vid[idx]
                self.current_letters[idx] = "_"

    def fresh(self, new_ctx):
        return WendPropagator(None, self.size, self.domain, self.board_var, self.board, self.w_map, self.l_map, self.pd, new_ctx)

    def _fixed(self, x, v):
        vid = x.get_id()
        idx = v.as_long()

        self.assigned[vid] = idx
        self.idx_to_vid[idx] = vid
        self.trail.append(vid)

        i, j = self.var_pos[vid]
        self.current_letters[idx] = self.board[i][j]

        word_start = self.w_map[idx]
        word_length = self.l_map[idx]
        pattern = "".join(self.current_letters[word_start:word_start + word_length]).lower()

        if not self.pd.exists(pattern):
            conflicting_vars = [
                self.var_of_id[self.idx_to_vid[p]]
                for p in range(word_start, word_start + word_length)
                if self.current_letters[p] != "_"
            ]
            self.conflict(conflicting_vars)


class WendSolver(GenericSolver):
    def __init__(self, size, board, words):
        super().__init__()
        self.size = size
        self.board = board
        self.words = words
        self.encoding = WendEncoding(size, board, words)

        self.word_layout = self.encoding.word_layout_variable()
        self.solver.add(
            self.encoding.word_domain(self.word_layout) +
            self.encoding.word_structure(self.word_layout)
            + self.encoding.unique_word_constraint(self.word_layout)
        )

        # Attach the propagator to this solver instance
        w_map, l_map = self.letter_map()
        self.domain = sum(words) + len(words)
        pd = PatternDict.load('src/utils/word_index.pkl')
        self.propagator = WendPropagator(self.solver, self.size, self.domain, self.word_layout, self.board, w_map, l_map, pd)

    def letter_map(self):
        word_map = {} # Maps each letter idx to its origin word
        length_map = {} # Maps each letter idx to the length of its origin word
        letter_count= 0
        for word in self.words:
            for letter in range(word):
                word_map[letter_count+letter] = letter_count
                length_map[letter_count+letter] = word
            letter_count += word + 1
        return word_map, length_map

    def get_model(self):
        words = ["_"] * self.domain
        solution = {'board': [["" for _ in range(self.size)] for _ in range(self.size)], 'words':[]}
        board = [[int(str(self.solver.model()[self.word_layout[j][i]])) for i in range(self.size)] for j in range(self.size)]
        solved_words = []
        letter_idx = 0
        for word in self.words:
            solved_words.append([i for i in range(letter_idx, letter_idx+word)])
            letter_idx += word + 1

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    idx = board[i][j]
                    words[idx] = self.board[i][j]
                    for idx, solved_word in enumerate(solved_words):
                        if board[i][j] in solved_word:
                            solution['board'][i][j] = str(idx)

        count = 0
        for word in self.words:
            solution['words'].append(words[count:count+word])
            count += word + 1


        return solution
