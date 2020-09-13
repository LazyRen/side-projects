# TETRIMINO COLORS
COLOR_I = (0,   159, 218)  # Light Blue
COLOR_J = (0,   101, 189)  # Dark Blue
COLOR_L = (255, 121, 0)  # Orange
COLOR_O = (254, 203, 0)  # Yellow
COLOR_S = (105, 190, 40)  # Green
COLOR_Z = (237, 41,  57)  # Red
COLOR_T = (149, 45,  152)  # Magenta

# TETRIMINO COLORS
SHAPE_I = [['....',
            '0000',
            '....',
            '....'],
           ['..0.',
            '..0.',
            '..0.',
            '..0.'],
            ['....',
            '....',
            '0000',
            '....'],
           ['.0..',
            '.0..',
            '.0..',
            '.0..']]

SHAPE_J = [['0..',
            '000',
            '...'],
           ['.00',
            '.0.',
            '.0.'],
           ['...',
            '000',
            '..0'],
           ['.0.',
            '.0.',
            '00.']]

SHAPE_L = [['..0',
            '000',
            '...'],
           ['.0.',
            '.0.',
            '.00'],
           ['...',
            '000',
            '0..'],
           ['00.',
            '.0.',
            '.0.']]

SHAPE_O = [['.00.',
            '.00.',
            '....']]

SHAPE_S = [['.00',
            '00.',
            '...'],
           ['.0.',
            '.00',
            '..0'],
           ['...',
            '.00',
            '00.'],
           ['0..',
            '00.',
            '.0.']]

SHAPE_Z = [['00.',
            '.00',
            '...'],
           ['..0',
            '.00',
            '.0.'],
           ['...',
            '00.',
            '.00'],
           ['.0.',
            '00.',
            '0..']]

SHAPE_T = [['.0.',
            '000',
            '...'],
           ['.0.',
            '.00',
            '.0.'],
           ['...',
            '000',
            '.0.'],
           ['.0.',
            '00.',
            '.0.']]

tetromino_shapes = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T]
tetromino_colors = [COLOR_I, COLOR_J, COLOR_L, COLOR_O, COLOR_S, COLOR_Z, COLOR_T]
# index 0 - 6 represent shape


class Tetromino():
    def __init__(self, shape, row=0, column=5):
        self.shape = shape
        self.row = row
        self.col = column
        self.color = tetromino_colors[tetromino_shapes.index(shape)]
        self.rotation = 0  # number from 0-3

    def reset(self):
        self.row = 0
        self.col = 5
        self.rotation = 0
        return self
