import pygame as pg
import sys
from sudoku_generator import generate_sudoku


def main_menu(screen):
    # Initialize Font
    title_font = pg.font.Font(None, 100)
    sub_font = pg.font.Font(None, 75)
    button_font = pg.font.Font(None, 60)

    # Initialize Colors
    bg_color = (60, 55, 68)
    text_color = (251, 255, 241)
    button_color = (48, 102, 190)

    # Render text to screen
    screen.fill(bg_color)
    title_surface = title_font.render("Sudoku", True, text_color)
    title_rectangle = title_surface.get_rect(center=(900 // 2, 900 // 2 - 250))
    sub_surface = sub_font.render("Pick a difficulty:", True, text_color)
    sub_rect = sub_surface.get_rect(center=(900 // 2, 900 // 2))

    screen.blit(title_surface, title_rectangle)
    screen.blit(sub_surface, sub_rect)

    buttons = ["Easy", "Medium", "Hard"]
    button_rects = []
    for i, text in enumerate(buttons):
        text_surface = button_font.render(text, True, text_color)
        button_surface = pg.Surface((text_surface.get_width() + 20, text_surface.get_height() + 20))
        button_surface.fill(button_color)
        button_surface.blit(text_surface, (10, 10))
        rect = button_surface.get_rect(center=(900 // 2, 900 // 2 + 100 + i * 100))
        screen.blit(button_surface, rect)
        button_rects.append(rect)

    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        # Return the number of empty cells based on difficulty
                        return 30 + 10 * i  # 30 for Easy, 40 for Medium, 50 for Hard


def play_screen(cells_removed, screen):
    def generate_sudoku_board(cells_removed):
        # Generate a Sudoku board with the specified number of empty cells
        return generate_sudoku(9, cells_removed)

    def is_board_solved(board):
        # to check if the Sudoku board is solved correctly
        pass

    def is_board_full(board):
        for row in board:
            if 0 in row:
                return False
        return True

    board = generate_sudoku_board(cells_removed)
    original_board = [row[:] for row in board]  # Copy of the original board
    font = pg.font.Font(None, 40)
    CELL_SIZE = 60
    GRID_ORIGIN = (50, 50)
    BLACK = (0, 0, 0)
    GREY = (200, 200, 200)
    selected_cell = None

    def draw_grid():
        for x in range(10):
            line_thickness = 4 if x % 3 == 0 else 1
            pg.draw.line(screen, BLACK, (GRID_ORIGIN[0] + x * CELL_SIZE, GRID_ORIGIN[1]),
                         (GRID_ORIGIN[0] + x * CELL_SIZE, GRID_ORIGIN[1] + 9 * CELL_SIZE), line_thickness)
            pg.draw.line(screen, BLACK, (GRID_ORIGIN[0], GRID_ORIGIN[1] + x * CELL_SIZE),
                         (GRID_ORIGIN[0] + 9 * CELL_SIZE, GRID_ORIGIN[1] + x * CELL_SIZE), line_thickness)

    def draw_numbers():
        for i in range(9):
            for j in range(9):
                cell_value = board[i][j]
                if cell_value != 0:
                    text = font.render(str(cell_value), True, BLACK)
                    screen.blit(text, (GRID_ORIGIN[0] + j * CELL_SIZE + 20, GRID_ORIGIN[1] + i * CELL_SIZE + 15))

    def draw_selected():
        if selected_cell:
            pg.draw.rect(screen, (255, 0, 0), (
            GRID_ORIGIN[0] + selected_cell[1] * CELL_SIZE, GRID_ORIGIN[1] + selected_cell[0] * CELL_SIZE, CELL_SIZE,
            CELL_SIZE), 3)

    def handle_mouse_click(pos):
        if pos[0] < GRID_ORIGIN[0] or pos[1] < GRID_ORIGIN[1] or pos[0] > GRID_ORIGIN[0] + 9 * CELL_SIZE or pos[1] > \
                GRID_ORIGIN[1] + 9 * CELL_SIZE:
            return None
        row = (pos[1] - GRID_ORIGIN[1]) // CELL_SIZE
        col = (pos[0] - GRID_ORIGIN[0]) // CELL_SIZE
        return (row, col)

    def draw_buttons():
        buttons = ["Reset", "Restart", "Exit"]
        button_actions = []
        for i, button in enumerate(buttons):
            button_rect = pg.Rect(50 + i * 250, 600, 200, 40)
            pg.draw.rect(screen, (180, 180, 255), button_rect)
            text = font.render(button, True, BLACK)
            screen.blit(text, (50 + i * 250 + 10, 600 + 10))
            button_actions.append((button_rect, button))
        return button_actions

    running = True
    while running:
        screen.fill(GREY)
        draw_grid()
        draw_numbers()
        draw_selected()
        button_actions = draw_buttons()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                selected_cell = handle_mouse_click(pos)
                for button_rect, action in button_actions:
                    if button_rect.collidepoint(pos):
                        if action == "Reset":
                            board = [row[:] for row in original_board]
                        elif action == "Restart":
                            main()
                        elif action == "Exit":
                            pg.quit()
                            sys.exit()
            elif event.type == pg.KEYDOWN and selected_cell:
                if event.unicode.isdigit():
                    num = int(event.unicode)
                    if original_board[selected_cell[0]][selected_cell[1]] == 0:  # Only modify empty cells
                        board[selected_cell[0]][selected_cell[1]] = num

        # Check if the game is over
        if is_board_full(board):
            if is_board_solved(board):
                game_won_screen(screen)
            else:
                game_over_screen(screen)

        pg.display.flip()


def game_over_screen(screen):
    font = pg.font.Font(None, 60)
    GREY = (60, 55, 68)

    screen.fill(GREY)
    text_surface = font.render("Game Over :(", True, (251, 255, 241))
    text_rect = text_surface.get_rect(center=(450, 200))
    screen.blit(text_surface, text_rect)

    button_rects = draw_game_over_buttons(screen)

    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for rect, action in button_rects:
                    if rect.collidepoint(event.pos):
                        if action == "Restart":
                            main()


def draw_game_over_buttons(screen):
    font = pg.font.Font(None, 40)
    button_rects = []
    buttons = ["Restart"]
    for i, text in enumerate(buttons):
        button_rect = pg.Rect(250, 400, 400, 80)
        pg.draw.rect(screen, (180, 180, 255), button_rect)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        button_rects.append((button_rect, text))
    return button_rects


def game_won_screen(screen):
    font = pg.font.Font(None, 60)
    GREY = (60, 55, 68)

    screen.fill(GREY)
    text_surface = font.render("Game Won!", True, (251, 255, 241))
    text_rect = text_surface.get_rect(center=(450, 200))
    screen.blit(text_surface, text_rect)

    button_rects = draw_game_won_buttons(screen)

    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for rect, action in button_rects:
                    if rect.collidepoint(event.pos):
                        if action == "Exit":
                            pg.quit()
                            sys.exit()


def draw_game_won_buttons(screen):
    font = pg.font.Font(None, 40)
    button_rects = []
    buttons = ["Exit"]
    for i, text in enumerate(buttons):
        button_rect = pg.Rect(250, 400, 400, 80)
        pg.draw.rect(screen, (180, 180, 255), button_rect)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        button_rects.append((button_rect, text))
    return button_rects


def main():
    pg.init()
    game = pg.display.set_mode((900, 900))
    pg.display.set_caption('Sudoku')
    cells_removed = main_menu(game)
    play_screen(cells_removed, game)
    pg.quit()


if __name__ == "__main__":
    main()
