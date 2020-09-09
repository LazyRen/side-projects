from copy import deepcopy
import random
import pygame

# original source code from "https://www.freecodecamp.org/news/tetris-python-tutorial-pygame/"
# Modified by DaeIn Lee

# Tetris Guideline
# http://brokenspine.org/Gaming/2009%20Tetris%20Design%20Guideline.pdf
# http://brokenspine.org/Gaming/2009%20Tetris%20Marketing%20Guideline.pdf
# https://tetris.fandom.com/wiki/Tetris_Guideline
# https://tetris.wiki/Tetris_Guideline

# GAME SETTING
FALL_SPEED       = 250
REPEAT_DELAY     = 250
REPEAT_INTERVAL  = 75

# CONSTANT VARIABLES
TOTAL_TETROMINOS = 7
NEXT_QUEUE_SIZE  = 3

# DISPLAY
WINDOW_WIDTH     = 800
WINDOW_HEIGHT    = 700
GRID_WIDTH       = 10
GRID_HEIGHT      = 20
GRID_BUFFER      = 2
TETROMINO_SIZE   = 5
BLOCK_SIZE       = 30
PLAY_WIDTH       = GRID_WIDTH  * BLOCK_SIZE
PLAY_HEIGHT      = GRID_HEIGHT * BLOCK_SIZE

TOP_LEFT_X       = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y       = WINDOW_HEIGHT - PLAY_HEIGHT

# OPTIONS

# RGB COLORS
BLACK   = (0,   0,   0  )
BLUE    = (0,   0,   255)
CYAN    = (0,   255, 255)
GRAY    = (128, 128, 128)
GREEN   = (0,   128, 0  )
LIME    = (0,   255, 0  )
MAGENTA = (255, 0,   255)
ORANGE  = (255, 165, 0  )
PURPLE  = (128, 0,   128)
RED     = (255, 0,   0  )
WHITE   = (255, 255, 255)
YELLOW  = (255, 255, 0  )

# TETRIMINO COLORS
COLOR_I = (0,   159, 218)  # Light Blue
COLOR_J = (0,   101, 189)  # Dark Blue
COLOR_L = (255, 121, 0  )  # Orange
COLOR_O = (254, 203, 0  )  # Yellow
COLOR_S = (105, 190, 40 )  # Green
COLOR_Z = (237, 41,  57 )  # Red
COLOR_T = (149, 45,  152)  # Magenta

# TETRIMINO FORMATS
# https://harddrop.com/wiki/File:SRS-true-rotations.png
# SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T
SHAPE_I = [['.....',
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

tetrominos       = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T]
tetromino_colors = [COLOR_I, COLOR_J, COLOR_L, COLOR_O, COLOR_S, COLOR_Z, COLOR_T]
# index 0 - 6 represent shape


class Piece():
    def __init__(self, shape, row=0, column=5):
        self.shape = shape
        self.row = row
        self.col = column
        self.color = tetromino_colors[tetrominos.index(shape)]
        self.rotation = 0  # number from 0-3

    def reset(self):
        self.row = 0
        self.col = 5
        self.rotation = 0
        return self


class RandomGenerator:
    def __init__(self):
        self.seven_bags = [deepcopy(tetrominos) for x in range(2)]
        for bag in self.seven_bags:
            random.shuffle(bag)
        self.cur_bag = 0
        self.cur_idx = 0

    def get_tetromino(self):
        ret = self.seven_bags[self.cur_bag][self.cur_idx]
        self.cur_idx += 1
        if self.cur_idx >= TOTAL_TETROMINOS:
            random.shuffle(self.seven_bags[self.cur_bag])
            self.cur_idx = 0
            self.cur_bag = (self.cur_bag + 1) % 2
        return Piece(ret)

    def get_next_piece_list(self):
        ret = []
        idx = self.cur_idx
        bag = self.cur_bag
        for _ in range(NEXT_QUEUE_SIZE):
            if idx >= TOTAL_TETROMINOS:
                idx = 0
                bag = (bag + 1) % 2
            ret.append(self.seven_bags[bag][idx])
            idx = idx + 1
        ret = [Piece(item) for item in ret]
        return ret


class GameStatus:
    def __init__(self):
        self.generator        = RandomGenerator()
        self.locked_positions = {}  # (r,c):(255,0,0)
        self.grid             = create_grid(self.locked_positions)
        self.curr_tetromino   = self.generator.get_tetromino()
        self.next_tetrominos  = self.generator.get_next_piece_list()
        self.hold_tetromino   = None
        self.is_holdable      = True


def create_grid(locked_positions):
    grid = [[(0, 0, 0) for x in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
    for r, _ in enumerate(grid):
        for c, _ in enumerate(grid[r]):
            if (r, c) in locked_positions:
                grid[r][c] = locked_positions[(r, c)]
    return grid


def convert_tetromino_format(tetromino):
    positions = []
    shape_format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]

    for r, line in enumerate(shape_format):
        row = list(line)
        for c, column in enumerate(row):
            if column == '0':
                positions.append((tetromino.row + r, tetromino.col + c))

    for idx, pos in enumerate(positions):
        positions[idx] = (pos[0] - 4, pos[1] - 2)
    return positions


def get_ghost_piece(status):
    ghost_piece = deepcopy(status.curr_tetromino)
    while valid_space(status.grid, ghost_piece):
        ghost_piece.row += 1
    ghost_piece.row -= 1
    return ghost_piece


def valid_space(grid, tetromino):
    accepted_positions = [[(r, c) for c in range(GRID_WIDTH) if grid[r][c] == (0, 0, 0)] for r in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_tetromino_format(tetromino)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[0] > -1 or pos[1] < 0 or pos[1] >= GRID_WIDTH:
                return False
    return True


def check_ground_hit(grid, tetromino):
    accepted_positions = [[(r, c) for c in range(
        GRID_WIDTH) if grid[r][c] == (0, 0, 0)] for r in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_tetromino_format(tetromino)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[0] > -1:
                return True
    return False


def check_lost(positions):
    for pos in positions:
        if pos[0] < 0:
            return True
    return False


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH  // 2 - label.get_width()  // 2,
                         TOP_LEFT_Y + PLAY_HEIGHT // 2 - label.get_height() // 2))


def draw_grid(surface, row, col):
    start_x = TOP_LEFT_X
    start_y = TOP_LEFT_Y
    for r in range(row):
        pygame.draw.line(surface, (128, 128, 128),
                         (start_x, start_y + r * BLOCK_SIZE), (start_x + PLAY_WIDTH, start_y + r * BLOCK_SIZE))  # horizontal lines
        for c in range(col):
            pygame.draw.line(surface, (128, 128, 128),
                             (start_x + c * BLOCK_SIZE, start_y), (start_x + c * BLOCK_SIZE, start_y + PLAY_HEIGHT))  # vertical lines


def clear_rows(status):
    grid = status.grid
    locked = status.locked_positions
    cleared = 0
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        if (0, 0, 0) not in row:
            cleared += 1
            highest = r
            for c in range(len(row)):
                locked.pop((r, c), None)
    if cleared > 0:
        for key in sorted(list(locked), key=lambda x: x[0])[::-1]:
            r, c = key
            if r < highest:
                new_key = (r + cleared, c)
                locked[new_key] = locked.pop(key)


def draw_next_tetromino(surface, next_tetrominos):
    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y

    font = pygame.font.SysFont('comicsans', BLOCK_SIZE)
    label = font.render('Next Queue', 1, WHITE)
    surface.blit(label, (start_x + (TETROMINO_SIZE * BLOCK_SIZE - label.get_width()) // 2, start_y))

    start_y += BLOCK_SIZE

    for idx, tetromino in enumerate(next_tetrominos):
        shape_format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
        # pygame.draw.rect(surface, WHITE, (start_x, start_y + idx * BLOCK_SIZE * TETROMINO_SIZE,
        #                                 BLOCK_SIZE * TETROMINO_SIZE, BLOCK_SIZE * TETROMINO_SIZE), 5)
        for r, line in enumerate(shape_format):
            row = list(line)
            for c, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, tetromino.color, (start_x + c * BLOCK_SIZE, start_y + r * BLOCK_SIZE + idx * BLOCK_SIZE * TETROMINO_SIZE,
                                                                BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_hold_tetromino(surface, hold_tetromino):
    if hold_tetromino is None:
        return
    start_x = TOP_LEFT_X - 150
    start_y = TOP_LEFT_Y

    font = pygame.font.SysFont('comicsans', BLOCK_SIZE)
    label = font.render('Hold', 1, WHITE)
    surface.blit(label, (start_x + (TETROMINO_SIZE * BLOCK_SIZE - label.get_width()) // 2, start_y))

    start_y += BLOCK_SIZE

    shape_format = hold_tetromino.shape[0]
    for r, line in enumerate(shape_format):
        row = list(line)
        for c, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, hold_tetromino.color,
                                    (start_x + c * BLOCK_SIZE,
                                    start_y + r * BLOCK_SIZE + TETROMINO_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_ghost_piece(surface, ghost_piece):
    ghost_piece_pos = convert_tetromino_format(ghost_piece)
    for r, c in ghost_piece_pos:
        if -1 < r < GRID_HEIGHT and -1 < c < GRID_WIDTH:
            pygame.draw.rect(surface, ghost_piece.color, (TOP_LEFT_X + c * BLOCK_SIZE, TOP_LEFT_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 3)


def draw_window(surface, grid):
    surface.fill(BLACK)
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - (label.get_width() // 2), BLOCK_SIZE))

    for r, _ in enumerate(grid):
        for c, _ in enumerate(grid[r]):
            pygame.draw.rect(surface, grid[r][c], (TOP_LEFT_X + c * BLOCK_SIZE, TOP_LEFT_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # draw grid and border
    draw_grid(surface, GRID_HEIGHT, GRID_WIDTH)
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


def swap_hold_tetromino(status):
    if status.is_holdable:
        if status.hold_tetromino is None:
            status.hold_tetromino = status.curr_tetromino.reset()
            status.curr_tetromino = status.generator.get_tetromino()
        else:
            status.curr_tetromino, status.hold_tetromino = status.hold_tetromino, status.curr_tetromino.reset()
        status.is_holdable = False


def keyboard_input_received():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return True
        if event.type == pygame.QUIT:
            pygame.quit()
    return False


def get_keyboard_input(status):
    prev_tetromino = deepcopy(status.curr_tetromino)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_F1:
                while True:
                    draw_text_middle("Game Paused", 40, WHITE, win)
                    pygame.display.update()
                    if keyboard_input_received():
                        break
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_c:
                swap_hold_tetromino(status)
                return
            elif event.key == pygame.K_UP or event.key == pygame.K_x:
                status.curr_tetromino.rotation = status.curr_tetromino.rotation + 1 % len(status.curr_tetromino.shape)
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_z:
                status.curr_tetromino.rotation = status.curr_tetromino.rotation - 1 % len(status.curr_tetromino.shape)
            elif event.key == pygame.K_DOWN:
                status.curr_tetromino.row += 1
            elif event.key == pygame.K_SPACE:  # Hard Drop(move Tetrimino to the bottom)
                while valid_space(status.grid, status.curr_tetromino):
                    status.curr_tetromino.row += 1
                status.curr_tetromino.row -= 1

    # Auto Repeat only works for left / right arrow key
    pygame.event.pump()
    key_states = pygame.key.get_pressed()
    if key_states[pygame.K_LEFT] and (get_keyboard_input.repeat_enabled == 0
                                      or (get_keyboard_input.repeat_enabled == 1 and get_keyboard_input.interval >= REPEAT_DELAY)
                                      or (get_keyboard_input.repeat_enabled >= 2 and get_keyboard_input.interval >= REPEAT_INTERVAL)):
        get_keyboard_input.repeat_enabled += 1
        get_keyboard_input.interval = 0
        status.curr_tetromino.col -= 1
    if key_states[pygame.K_RIGHT] and (get_keyboard_input.repeat_enabled == 0
                                      or (get_keyboard_input.repeat_enabled == 1 and get_keyboard_input.interval >= REPEAT_DELAY)
                                      or (get_keyboard_input.repeat_enabled >= 2 and get_keyboard_input.interval >= REPEAT_INTERVAL)):
        get_keyboard_input.repeat_enabled += 1
        get_keyboard_input.interval = 0
        status.curr_tetromino.col += 1
    if not key_states[pygame.K_LEFT] and not key_states[pygame.K_RIGHT]:
        get_keyboard_input.repeat_enabled = 0

    if not valid_space(status.grid, status.curr_tetromino):
        status.curr_tetromino = prev_tetromino


def main():
    status    = GameStatus()
    lock_down = False
    clock     = pygame.time.Clock()
    fall_time = 0

    get_keyboard_input.repeat_enabled = 0
    get_keyboard_input.interval       = 0

    while True:
        status.grid = create_grid(status.locked_positions)
        raw_time = clock.get_rawtime()
        fall_time += raw_time
        get_keyboard_input.interval += raw_time
        clock.tick()
        # PIECE FALLING CODE
        if fall_time >= FALL_SPEED:
            fall_time = 0
            status.curr_tetromino.row += 1
            if check_ground_hit(status.grid, status.curr_tetromino) and status.curr_tetromino.row > 0:
                status.curr_tetromino.row -= 1
                lock_down = True

        get_keyboard_input(status)
        tetromino_pos = convert_tetromino_format(status.curr_tetromino)
        ghost_piece = get_ghost_piece(status)

        # Add piece to the grid for drawing
        for r, c in tetromino_pos:
            if -1 < r < GRID_HEIGHT and -1 < c < GRID_WIDTH:
                status.grid[r][c] = status.curr_tetromino.color

        # Piece drops onto a surface
        if lock_down:
            for pos in tetromino_pos:
                status.locked_positions[pos] = status.curr_tetromino.color
            status.curr_tetromino = status.generator.get_tetromino()
            status.next_tetrominos = status.generator.get_next_piece_list()
            status.is_holdable = True
            ghost_piece = get_ghost_piece(status)
            lock_down = False
            clear_rows(status)
            if check_lost(status.locked_positions):
                break

        draw_window(win, status.grid)
        draw_ghost_piece(win, ghost_piece)
        draw_next_tetromino(win, status.next_tetrominos)
        draw_hold_tetromino(win, status.hold_tetromino)
        pygame.display.update()

    while True:
        draw_text_middle("You Lost", 40, WHITE, win)
        pygame.display.update()
        if keyboard_input_received():
            break


def main_menu():
    while True:
        win.fill(BLACK)
        draw_text_middle('Press any key to begin.', 60, WHITE, win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main()
            elif event.type == pygame.QUIT:
                pygame.quit()


if __name__ == '__main__':
    pygame.font.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_menu()  # start game
