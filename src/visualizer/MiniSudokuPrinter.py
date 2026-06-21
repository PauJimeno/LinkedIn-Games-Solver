class MiniSudokuPrinter:
    def __init__(self, solution, size, background):
        self.solution = solution
        self.size = size
        self.background = background

    def solution_to_terminal(self):
        alternator = 0
        cell = '\u001B[48;2;{};{};{}m\u001B[38;2;0;0;0m{}\u001B[0m'
        for i in range(self.size):
            for j in range(self.size):
                char = f" {self.solution[i][j]} "
                b_r, b_g, b_b = self.background[alternator][0], self.background[alternator][1], self.background[alternator][2]
                print(cell.format(b_r, b_g, b_b, char), end='')
                alternator = not alternator
            if self.size % 2 == 0:
                alternator = not alternator
            print()
