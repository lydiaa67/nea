import pygame
from .constants import BLACK, RED, BLUE, SQUARE_SIZE, WIDTH, HEIGHT, COLS, ROWS, get_font, piece_sound
from .board import Board

class Game:
    def __init__(self, win, ):
        self.win = win
        self.BLACK_time = 900  # same as 15 mins
        self.turn_start_time = pygame.time.get_ticks()  # Start tracking time
        self._init()

    def update(self):
        self.update_timer()  # Update countdown
        self.board.draw(self.win)
        from menu import difficulty
        if difficulty != "hard":
            self.draw_valid_moves(self.valid_moves)
        self.draw_timer()  # Display updated timer
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()  # Ensure the board is initialized here
        self.turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:  # since you cannot move into a position with another piece
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            piece_sound.play()  # Play sound for player move
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            offset_x = (800 - (SQUARE_SIZE * COLS)) // 2  # Same centering offset
            pygame.draw.circle(self.win, BLUE, (offset_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, 52 + row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = RED
        else:
            from menu import difficulty
            if difficulty == "easy":
                self.BLACK_time += 20
            self.turn = BLACK
        self.turn_start_time = pygame.time.get_ticks()  # Reset time tracking when turn changes

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def draw_timer(self):
        minutes = int(self.BLACK_time) // 60
        seconds = int(self.BLACK_time) % 60
        timer_text = get_font(25).render(f"Time Left: {minutes}:{seconds:02d}", True, "White")

        # Draw a black background for the timer in the top 52 pixels
        pygame.draw.rect(self.win, (127, 9, 9), (0, 0, WIDTH, 52))

        # Center the timer text within the 52px tall area
        self.win.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 52 // 2 - timer_text.get_height() // 2))

    def update_timer(self):
        if self.turn == BLACK:  # Only count down when it's BLACK's turn
            elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) / 1000  # Time in seconds
            self.BLACK_time = max(0, self.BLACK_time - elapsed_time)  # Prevent negative time
            self.turn_start_time = pygame.time.get_ticks()  # Reset timer start

