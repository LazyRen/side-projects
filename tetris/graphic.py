import pygame
from tetromino import *
from variables import *


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


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - label.get_width() // 2,
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


def draw_next_tetromino(surface, next_tetrominoes):
    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y

    font = pygame.font.SysFont('comicsans', BLOCK_SIZE)
    label = font.render('Next Queue', 1, WHITE)
    surface.blit(label, (start_x + (TETROMINO_SIZE
                                    * BLOCK_SIZE - label.get_width()) // 2, start_y))

    start_y += BLOCK_SIZE

    for idx, tetromino in enumerate(next_tetrominoes):
        shape_format = tetromino.shape[tetromino.rotation % len(
            tetromino.shape)]
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
    surface.blit(label, (start_x + (TETROMINO_SIZE
                                    * BLOCK_SIZE - label.get_width()) // 2, start_y))

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
            pygame.draw.rect(surface, ghost_piece.color, (TOP_LEFT_X + c
                                                          * BLOCK_SIZE, TOP_LEFT_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 3)


def draw_window(surface, grid):
    surface.fill(BLACK)
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2
                         - (label.get_width() // 2), BLOCK_SIZE))

    for r, _ in enumerate(grid):
        for c, _ in enumerate(grid[r]):
            pygame.draw.rect(surface, grid[r][c], (TOP_LEFT_X + c * BLOCK_SIZE,
                                                   TOP_LEFT_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # draw grid and border
    draw_grid(surface, GRID_HEIGHT, GRID_WIDTH)
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y,
                                    PLAY_WIDTH, PLAY_HEIGHT), 5)
