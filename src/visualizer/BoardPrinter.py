from PIL import Image, ImageDraw, ImageFont


class BoardPrinter:
    def __init__(self, board, size, solution, color_palette=None):
        self.board = board
        self.solution = solution
        self.size = size
        if color_palette is None:
            self.color_palette = {
                '0': (255, 255, 255),       # White
                '1': (128, 0, 0),           # Maroon
                '2': (170, 110, 40),        # Brown
                '3': (128, 128, 0),         # Olive
                '4': (0, 128, 128),         # Teal
                '5': (220, 190, 255),       # Lavender
                '6': (230, 25, 75),         # Red
                '7': (245, 130, 48),        # Orange
                '8': (255, 225, 25),        # Yellow
                '9': (210, 245, 60),        # Lime
                '10': (60, 180, 75),        # Green
                '11': (70, 240, 240),       # Cyan
                '12': (0, 130, 200),        # Blue
                '13': (145, 30, 180),       # Purple
                '14': (240, 50, 230),       # Magenta
                '15': (128, 128, 128),      # Grey
                '16': (250, 190, 212),      # Pink
                '17': (255, 215, 180),      # Apricot
                '18': (255, 250, 200),      # Beige
                '19': (170, 255, 195),      # Mint
                '20': (0, 0, 128),          # Navy
            }
        else:
            self.color_palette = color_palette

    def solution_to_terminal(self):
        cell = '\u001B[48;2;{};{};{}m\u001B[38;2;0;0;0m {} \u001B[0m'
        for i in range(self.size):
            for j in range(self.size):
                r, g, b = self.color_palette[self.board[i][j]]
                char = 'x' if self.solution[j] == i else ' '
                print(cell.format(r, g, b, char), end='')
            print()

    def solution_as_image(self, filename):
        cell_size = 50
        img_size = self.size * cell_size
        image = Image.new('RGB', (img_size, img_size), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Draw cell info
        font = ImageFont.load_default(size=30)

        for i in range(self.size):
            for j in range(self.size):
                r, g, b = self.color_palette[self.board[i][j]]
                top_left = (j * cell_size, i * cell_size)
                bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
                draw.rectangle([top_left, bottom_right], fill=(r, g, b))
                if self.solution[j] == i:
                    text = 'x'
                    text_width, text_height = draw.textbbox((0, 0), text, font=font)[
                                              2:4]  # Get width and height of the text
                    text_position = (
                    j * cell_size + (cell_size - text_width) / 2, i * cell_size + (cell_size - text_height) / 2)
                    draw.text(text_position, text, fill=(0, 0, 0), font=font)

        # Draw grid lines
        for i in range(self.size + 1):
            # Horizontal lines
            draw.line((0, i * cell_size, img_size, i * cell_size), fill=(0, 0, 0), width=3)
            # Vertical lines
            draw.line((i * cell_size, 0, i * cell_size, img_size), fill=(0, 0, 0), width=3)

        image.save(filename)
