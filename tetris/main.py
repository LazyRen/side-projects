import random
import pygame
from copy import deepcopy

# 10 x 20 square grid
# shapes: S, Z, I, O, J, L, T
# represented in order by 0 - 6

pygame.font.init()

# GLOBALS VARS
FALL_SPEED      = 25
WINDOW_WIDTH    = 800
WINDOW_HEIGHT   = 700
GRID_WIDTH      = 10
GRID_HEIGHT     = 20
SHAPE_SIZE      = 4
BLOCK_SIZE      = 30
PLAY_WIDTH      = GRID_WIDTH  * BLOCK_SIZE
PLAY_HEIGHT     = GRID_HEIGHT * BLOCK_SIZE

TOP_LEFT_X      = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y      = WINDOW_HEIGHT - PLAY_HEIGHT

# SHAPE FORMATS
# https://harddrop.com/wiki/File:SRS-true-rotations.png
# SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T
SHAPE_I = [['..0..',
            '..0..',
            '..0..',
            '..0..',
            '.....'],
            ['.....',
            '..0..',
            '..0..',
            '..0..',
            '..0..'],
           ['.....',
            '.....',
            '0000.',
            '.....',
            '.....']]

SHAPE_J = [['.....',
            '.0...',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..00.',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '...0.',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '.00..',
            '.....']]

SHAPE_L = [['.....',
            '...0.',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '..00.',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '.0...',
            '.....'],
           ['.....',
            '.00..',
            '..0..',
            '..0..',
            '.....']]

SHAPE_O = [['.....',
            '.....',
            '.00..',
            '.00..',
            '.....']]

SHAPE_S = [['....',
            '..00',
            '.00.',
            '....'],
           ['.0..',
            '.00.',
            '..0.',
            '....']]

SHAPE_Z = [['.....',
            '.....',
            '.00..',
            '..00.',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '.0...',
            '.....']]

SHAPE_T = [['.....',
            '..0..',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..00.',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '..0..',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '..0..',
            '.....']]

shapes = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece():
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions=None):
    grid = [[(0, 0, 0) for x in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
    for r, _ in enumerate(grid):
        for c, _ in enumerate(grid[r]):
            if (c, r) in locked_positions:
                grid[r][c] = locked_positions[(c, r)]
    return grid


def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for r, line in enumerate(shape_format):
        row = list(line)
        for c, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + c, shape.y + r))

    for r, pos in enumerate(positions):
        positions[r] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == (0, 0, 0)] for i in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[0] < 0 or pos[0] >= GRID_WIDTH or pos[1] > -1:
                return False

    return True


def check_ground_hit(shape, grid):
    accepted_positions = [[(j, i) for j in range(
        GRID_WIDTH) if grid[i][j] == (0, 0, 0)] for i in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return True

    return False


def check_lost(positions):
    for pos in positions:
        if pos[1] < 0:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH  // 2  - label.get_width()  // 2,
                         TOP_LEFT_Y + PLAY_HEIGHT // 2 - label.get_height() // 2))


def draw_grid(surface, row, col):
    start_x = TOP_LEFT_X
    start_y = TOP_LEFT_Y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128),
                         (start_x, start_y + i * BLOCK_SIZE), (start_x + PLAY_WIDTH, start_y + i * BLOCK_SIZE))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128),
                             (start_x + j * BLOCK_SIZE, start_y), (start_x + j * BLOCK_SIZE, start_y + PLAY_HEIGHT))  # vertical lines


# need to see if row is clear then shift every other row above down one
def clear_rows(grid, locked):

    inc = 0
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        if (0, 0, 0) not in row:
            inc += 1
            ind = r
            for c in range(len(row)):
                locked.pop((c, r), None)
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', BLOCK_SIZE)
    label = font.render('Next Shape', 1, (255, 255, 255))

    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for r, line in enumerate(shape_format):
        row = list(line)
        for c, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (start_x + c * BLOCK_SIZE, start_y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    surface.blit(label, (start_x + (SHAPE_SIZE * BLOCK_SIZE - label.get_width()) // 2, start_y - BLOCK_SIZE))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - (label.get_width() // 2), BLOCK_SIZE))

    for r, _ in enumerate(grid):
        for c, _ in enumerate(grid[r]):
            pygame.draw.rect(surface, grid[r][c], (TOP_LEFT_X + c * BLOCK_SIZE, TOP_LEFT_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # draw grid and border
    draw_grid(surface, GRID_HEIGHT, GRID_WIDTH)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    # pygame.display.update()


def get_keyboard_input(current_piece, grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            prev_piece = deepcopy(current_piece)
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
            elif event.key == pygame.K_RIGHT:
                current_piece.x += 1
            elif event.key == pygame.K_UP:     # rotate shape
                current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
            elif event.key == pygame.K_DOWN:   # move shape one block down
                current_piece.y += 1
            elif event.key == pygame.K_SPACE:  # move shape to bottom
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1

            if not valid_space(current_piece, grid):
                current_piece = prev_piece

    return current_piece


def main():
    # global grid
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while True:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        # PIECE FALLING CODE
        if fall_time/10 >= FALL_SPEED:
            fall_time = 0
            current_piece.y += 1
            if check_ground_hit(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        current_piece = get_keyboard_input(current_piece, grid)

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for x, y in shape_pos:
            if -1 < y < GRID_HEIGHT and -1 < x < GRID_WIDTH:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)
            if check_lost(locked_positions):
                break

        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    while True:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main()
            elif event.type == pygame.QUIT:
                pygame.quit()


if __name__ == '__main__':
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tetris')
    pygame.key.set_repeat(FALL_SPEED * 4, FALL_SPEED * 2)
    main_menu()  # start game
