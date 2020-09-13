from copy import deepcopy
import random
import pygame
from graphic import *

# original source code from "https://www.freecodecamp.org/news/tetris-python-tutorial-pygame/"
# Modified by DaeIn Lee

# Tetris Guideline
# http://brokenspine.org/Gaming/2009%20Tetris%20Design%20Guideline.pdf
# http://brokenspine.org/Gaming/2009%20Tetris%20Marketing%20Guideline.pdf
# https://tetris.fandom.com/wiki/Tetris_Guideline
# https://tetris.wiki/Tetris_Guideline

# TETRIMINO FORMATS
# https://harddrop.com/wiki/File:SRS-true-rotations.png
# SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T


class RandomGenerator:
    def __init__(self):
        self.seven_bags = [deepcopy(tetromino_shapes) for x in range(2)]
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
        return Tetromino(ret)

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
        ret = [Tetromino(item) for item in ret]
        return ret


class GameStatus:
    def __init__(self):
        self.generator        = RandomGenerator()
        self.locked_positions = {}  # (r,c):(255,0,0)
        self.grid             = create_grid(self.locked_positions)
        self.curr_tetromino   = self.generator.get_tetromino()
        self.next_tetrominoes  = self.generator.get_next_piece_list()
        self.hold_tetromino   = None
        self.is_holdable      = True


def valid_space(grid, tetromino):
    accepted_positions = [[(r, c) for c in range(GRID_WIDTH) if grid[r][c] == (0, 0, 0)] for r in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_tetromino_format(tetromino)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[0] > -1 or pos[1] < 0 or pos[1] >= GRID_WIDTH:
                return False
    return True


def get_ghost_piece(status):
    ghost_piece = deepcopy(status.curr_tetromino)
    while valid_space(status.grid, ghost_piece):
        ghost_piece.row += 1
    ghost_piece.row -= 1
    return ghost_piece


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

        # Tetromino drops onto a surface
        if lock_down:
            for pos in tetromino_pos:
                status.locked_positions[pos] = status.curr_tetromino.color
            status.curr_tetromino = status.generator.get_tetromino()
            status.next_tetrominoes = status.generator.get_next_piece_list()
            status.is_holdable = True
            ghost_piece = get_ghost_piece(status)
            lock_down = False
            clear_rows(status)
            if check_lost(status.locked_positions):
                break

        draw_window(win, status.grid)
        draw_ghost_piece(win, ghost_piece)
        draw_next_tetromino(win, status.next_tetrominoes)
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
