class WendPrinter:
    def __init__(self, solution, words, size, board, colours):
        self.solution = solution
        self.words = words
        self.size = size
        self.board = board
        self.colours = colours

    def solution_to_terminal(self):
        cell = '\u001B[48;2;{};{};{}m\u001B[38;2;0;0;0m{}\u001B[0m'
        for i in range(self.size):
            for j in range(self.size):
                char = f' {self.board[i][j]} ' if self.board[i][j] else '   '
                idx = self.solution[i][j]
                hex_colour = self.colours[idx] if idx else 'B2B2B2'
                r = int(hex_colour[0:2], 16)
                g = int(hex_colour[2:4], 16)
                b = int(hex_colour[4:6], 16)
                print(cell.format(r, g, b, char), end='')
            print()

        cell  = '\u001B[38;2;{};{};{}m{}\u001B[0m'
        for idx, word in enumerate(self.words):
            for letter in word:
                char = f' {letter} '
                hex_colour = self.colours[str(idx)]
                r = int(hex_colour[0:2], 16)
                g = int(hex_colour[2:4], 16)
                b = int(hex_colour[4:6], 16)
                print(cell.format(r, g, b, char), end='')
            print()
