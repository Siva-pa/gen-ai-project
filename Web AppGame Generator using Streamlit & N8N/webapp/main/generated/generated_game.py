import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
FONT_SIZE_HEADER = 36
FONT_SIZE_MESSAGE = 28
FONT_SIZE_CELL = 120
FONT_SIZE_BUTTON = 30

font_header = pygame.font.Font(None, FONT_SIZE_HEADER)
font_message = pygame.font.Font(None, FONT_SIZE_MESSAGE)
font_cell = pygame.font.Font(None, FONT_SIZE_CELL)
font_button = pygame.font.Font(None, FONT_SIZE_BUTTON)

# Game variables
BOARD_SIZE = 3
BOARD_LINE_WIDTH = 10
board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 'X'
winner = None
game_over = False
player_names = {'X': "Player 1", 'O': "Player 2"}
scores = {'X': 0, 'O': 0}

# UI Layout dimensions
HEADER_HEIGHT = 100
MESSAGE_HEIGHT = 80
GAME_AREA_Y = HEADER_HEIGHT
GAME_AREA_H = HEIGHT - HEADER_HEIGHT - MESSAGE_HEIGHT
GAME_AREA_W = WIDTH

# Calculate cell size to fit centered game area
CELL_SIZE = min(GAME_AREA_W, GAME_AREA_H) // BOARD_SIZE
BOARD_OFFSET_X = (WIDTH - CELL_SIZE * BOARD_SIZE) // 2
BOARD_OFFSET_Y = GAME_AREA_Y + (GAME_AREA_H - CELL_SIZE * BOARD_SIZE) // 2

# Reset button
reset_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 70, 150, 50)

def ask_player_names():
    global player_names
    input_box_p1 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 40)
    input_box_p2 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 40)
    color_inactive = GRAY
    color_active = BLUE
    color_p1 = color_active
    color_p2 = color_inactive
    active_p1 = True
    active_p2 = False
    text_p1 = "Player 1"
    text_p2 = "Player 2"

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_p1.collidepoint(event.pos):
                    active_p1 = True
                    active_p2 = False
                elif input_box_p2.collidepoint(event.pos):
                    active_p2 = True
                    active_p1 = False
                else:
                    active_p1 = False
                    active_p2 = False
                color_p1 = color_active if active_p1 else color_inactive
                color_p2 = color_active if active_p2 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active_p1:
                    if event.key == pygame.K_RETURN:
                        active_p1 = False
                        active_p2 = True
                        color_p1 = color_inactive
                        color_p2 = color_active
                    elif event.key == pygame.K_BACKSPACE:
                        text_p1 = text_p1[:-1]
                    else:
                        text_p1 += event.unicode
                elif active_p2:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text_p2 = text_p2[:-1]
                    else:
                        text_p2 += event.unicode

        SCREEN.fill(WHITE)

        # Draw prompt
        prompt_text = font_header.render("Enter Player Names", True, BLACK)
        prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        SCREEN.blit(prompt_text, prompt_rect)

        # Player 1 Input Box
        pygame.draw.rect(SCREEN, color_p1, input_box_p1, 2)
        text_surface_p1 = font_message.render(text_p1 if text_p1 else "Player 1", True, BLACK)
        SCREEN.blit(text_surface_p1, (input_box_p1.x + 5, input_box_p1.y + 5))
        input_box_p1.w = max(300, text_surface_p1.get_width() + 10)

        # Player 2 Input Box
        pygame.draw.rect(SCREEN, color_p2, input_box_p2, 2)
        text_surface_p2 = font_message.render(text_p2 if text_p2 else "Player 2", True, BLACK)
        SCREEN.blit(text_surface_p2, (input_box_p2.x + 5, input_box_p2.y + 5))
        input_box_p2.w = max(300, text_surface_p2.get_width() + 10)

        pygame.display.flip()

    player_names['X'] = text_p1 if text_p1 else "Player 1"
    player_names['O'] = text_p2 if text_p2 else "Player 2"

def draw_header():
    pygame.draw.rect(SCREEN, GRAY, (0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.line(SCREEN, BLACK, (0, HEADER_HEIGHT), (WIDTH, HEADER_HEIGHT), 2)

    # Player 1 (X)
    name_x_text = font_header.render(f"{player_names['X']} (X): {scores['X']}", True, BLACK)
    name_x_rect = name_x_text.get_rect(center=(WIDTH // 4, HEADER_HEIGHT // 2))
    SCREEN.blit(name_x_text, name_x_rect)

    # Player 2 (O)
    name_o_text = font_header.render(f"{player_names['O']} (O): {scores['O']}", True, BLACK)
    name_o_rect = name_o_text.get_rect(center=(3 * WIDTH // 4, HEADER_HEIGHT // 2))
    SCREEN.blit(name_o_text, name_o_rect)

def draw_board():
    # Draw grid lines
    for i in range(1, BOARD_SIZE):
        # Vertical lines
        pygame.draw.line(SCREEN, BLACK,
                         (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y),
                         (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE),
                         BOARD_LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(SCREEN, BLACK,
                         (BOARD_OFFSET_X, BOARD_OFFSET_Y + i * CELL_SIZE),
                         (BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET_Y + i * CELL_SIZE),
                         BOARD_LINE_WIDTH)

    # Draw X's and O's
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            center_x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
            center_y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
            if board[row][col] == 'X':
                text_x = font_cell.render('X', True, RED)
                text_rect_x = text_x.get_rect(center=(center_x, center_y))
                SCREEN.blit(text_x, text_rect_x)
            elif board[row][col] == 'O':
                text_o = font_cell.render('O', True, BLUE)
                text_rect_o = text_o.get_rect(center=(center_x, center_y))
                SCREEN.blit(text_o, text_rect_o)

def draw_messages():
    pygame.draw.rect(SCREEN, GRAY, (0, HEIGHT - MESSAGE_HEIGHT, WIDTH, MESSAGE_HEIGHT))
    pygame.draw.line(SCREEN, BLACK, (0, HEIGHT - MESSAGE_HEIGHT), (WIDTH, HEIGHT - MESSAGE_HEIGHT), 2)

    msg = ""
    if winner:
        msg = f"{player_names[winner]} ({winner}) wins!"
    elif game_over:
        msg = "It's a draw!"
    else:
        msg = f"{player_names[current_player]}'s ({current_player}) turn"

    message_text = font_message.render(msg, True, BLACK)
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT - MESSAGE_HEIGHT // 2))
    SCREEN.blit(message_text, message_rect)

    if game_over:
        pygame.draw.rect(SCREEN, GREEN, reset_button_rect)
        pygame.draw.rect(SCREEN, BLACK, reset_button_rect, 2)
        button_text = font_button.render("Play Again", True, WHITE)
        button_text_rect = button_text.get_rect(center=reset_button_rect.center)
        SCREEN.blit(button_text, button_text_rect)

def check_win():
    # Check rows
    for row in range(BOARD_SIZE):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return board[row][0]
    # Check columns
    for col in range(BOARD_SIZE):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def check_draw():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                return False
    return True

def reset_game():
    global board, current_player, winner, game_over
    board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 'X'
    winner = None
    game_over = False

def main_game_loop():
    global current_player, winner, game_over

    running = True
    clock = pygame.time.Clock()
    FPS = 60

    ask_player_names()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if reset_button_rect.collidepoint(event.pos):
                        reset_game()
                elif winner is None: # Only allow moves if no winner yet and game is not a draw
                    mouse_x, mouse_y = event.pos

                    # Check if click is within the playable game area
                    if BOARD_OFFSET_X <= mouse_x < BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE and \
                       BOARD_OFFSET_Y <= mouse_y < BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE:
                        
                        col = (mouse_x - BOARD_OFFSET_X) // CELL_SIZE
                        row = (mouse_y - BOARD_OFFSET_Y) // CELL_SIZE

                        if board[row][col] == '':
                            board[row][col] = current_player
                            winner = check_win()
                            if winner:
                                game_over = True
                                scores[winner] += 1
                            elif check_draw():
                                game_over = True
                            else:
                                current_player = 'O' if current_player == 'X' else 'X'

        # Drawing
        SCREEN.fill(WHITE)
        draw_header()
        draw_board()
        draw_messages()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_game_loop()