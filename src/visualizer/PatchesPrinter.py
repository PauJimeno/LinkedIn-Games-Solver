class PatchesPrinter:
    def __init__(self, solution, size, hints, colours):
        self.solution = solution
        self.size = size
        self.hints = hints
        self.colours = colours

    def solution_to_terminal(self):
        cell = '\u001B[48;2;{};{};{}m\u001B[38;2;255;255;255m{}\u001B[0m'
        for i in range(self.size):
            for j in range(self.size):
                idx = i*self.size+j
                hint_idx = self.solution[i][j]
                char = f' {self.hints[hint_idx][1]} ' if len(self.hints[hint_idx])==2 and hint_idx==idx else '   '
                hex_colour = self.colours[hint_idx]
                r = int(hex_colour[0:2], 16)
                g = int(hex_colour[2:4], 16)
                b = int(hex_colour[4:6], 16)
                print(cell.format(r, g, b, char), end='')
            print()
