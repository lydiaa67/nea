import pygame
import sys
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, RED, COLS, ROWS, piece_sound
from checkers.game import Game
from minimax.algorithm import minimax
from checkers.board import Board
from music import play_next_song, control_music, skip_music, stop_music
from stats import Database_for_stats

timer_height = 70
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # win means window
pygame.display.set_caption('Checkers')

FPS = 60  # not in constants folder as it is not specific to the game, rather the display

def get_row_col_from_mouse(pos):
    x, y = pos
    offset_x = (800 - (SQUARE_SIZE * COLS)) // 2  # Centering offset
    x_adjusted = x - offset_x  # Shift x-coordinate back to board's actual position

    # Only process clicks inside the board area
    if not (0 <= x_adjusted < SQUARE_SIZE * COLS and 70 <= y < 70 + (SQUARE_SIZE * ROWS)):
        return None  # This prevents crashes when clicking outside

    row = (y - 70) // SQUARE_SIZE  # Adjust for timer space
    col = x_adjusted // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    stats = Database_for_stats()
    total_nodes = 0  # Initialises total_nodes
    turn_start_time = pygame.time.get_ticks()

    difficulty = None
    from menu import settings
    choice = settings()
    if choice in ["easy", "medium", "hard"]:
        difficulty = choice

    d_count = 0
    global depth
    if difficulty == "easy":
        depth = 3
    elif difficulty == "medium":
        depth = 4
    else: #hard
        depth = 5
    

    pygame.mixer.music.play(-1) 

    while run and (((pygame.time.get_ticks() - turn_start_time) / 1000) < game.BLACK_time):
        clock.tick(FPS)
        game.board.dynamic_depth(d_count, depth)

        if game.turn == RED:
            value, new_board, nodes_evaluated = minimax(game.get_board(), difficulty, True, game)
            total_nodes += nodes_evaluated
            game.ai_move(new_board)
            piece_sound.play()

        winner = game.winner()  # Store winner once

        if winner:
            print(winner)
            pygame.time.delay(2000)
            run = False
            break

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
                stop_music()
                stats.update_stats("draw", difficulty)
                run = False

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                stats.update_stats("draw", difficulty)
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                play_next_song()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row_col = get_row_col_from_mouse(pos)

                if row_col is not None:
                    row, col = row_col
                    game.select(row, col)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                control_music()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                skip_music()
            
            game.update()

    winner = game.winner()
    seconds = (pygame.time.get_ticks() - turn_start_time) / 1000
    print(f"You took: {seconds} seconds to win/lose")
    print(f"Total nodes evaluated by AI: {total_nodes}")

    if winner == "RED wins!" or seconds >= game.BLACK_time:
        stats.update_stats("loss", difficulty)
        from menu import loser  # Import inside function
        loser()
    elif winner == "BLACK wins!":
        stats.update_stats("win", difficulty)
        from menu import winner  # Import inside function
        winner()

# Move this import inside the function to prevent circular import
if __name__ == "__main__":
    from menu import main_menu
    main_menu()
