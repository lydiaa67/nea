import pygame.mixer
import copy
import time
from .constants import BLACK, ROWS, BLACK, SQUARE_SIZE, COLS, RED, SCREEN
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.BLACK_left = self.RED_left = 12
        self.BLACK_kings = self.RED_kings = 0
        self.create_board()

    def dynamic_depth(self, d_count, depth):
        if (d_count == 0) and ((self.BLACK_left <= 3) or (self.RED_left <= 3) or ((self.BLACK_kings + self.RED_kings) / (self.BLACK_left + self.RED_left) >= 0.5) or (self.BLACK_left == self.BLACK_kings) or (self.RED_left == self.RED_kings)):
            depth += 1

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0 and not piece.king:
            piece.make_king()
            if piece.color == RED:
                self.RED_kings += 1
            else:
                self.BLACK_kings += 1 

    def draw_squares(self, win):
        pygame.display.set_caption("Droughts game")
        board_background = pygame.image.load("assets/board_background.png")
        SCREEN.blit(board_background, (0, 0)) 
        offset_x = (800 - (SQUARE_SIZE * COLS)) // 2  # Centering offset (52 pixels)
        
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE + offset_x, row * SQUARE_SIZE + 52, SQUARE_SIZE, SQUARE_SIZE))
    
    def evaluate(self):
        heuristic_value = 0 #initial state

        # weightings
        piece_weight = 1
        king_weight = 0.5
        back_row_weight = 0.1
        middle_control_weight = 0.15
        vulnerable_pieces_weight = -0.2
        strategic_block_weight = 0.25

        # count of all pieces and their type for RED (AI)
        regular_pieces_RED = 0
        king_pieces_RED = 0
        back_row_RED = 0
        middle_control_RED = 0
        strategic_block_RED = 0
        vulnerable_pieces_RED = 0
        
        #count of all pieces and their types for BLACK (player)
        regular_pieces_BLACK = 0
        king_pieces_BLACK = 0
        back_row_BLACK = 0
        middle_control_BLACK = 0
        strategic_block_BLACK = 0
        vulnerable_pieces_BLACK = 0

        for row in range(ROWS):  # iterate through all pieces on the board
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    if piece.color == RED:
                        regular_pieces_RED += 1
                        if piece.king:
                            king_pieces_RED += 1
                        if row < 2:
                            back_row_RED += 1
                        if 2 <= row < 5 and 2 <= col < 6:
                            middle_control_RED += 1
                        if 2 <= row < 5 and (col < 2 or col > 5):
                            strategic_block_RED += 1
                        if piece.can_be_taken(self.board):
                            vulnerable_pieces_RED += 1
                    else:
                        regular_pieces_BLACK += 1
                        if piece.king:
                            king_pieces_BLACK += 1
                        if row > ROWS - 3:
                            back_row_BLACK += 1
                        if 2 <= row < 5 and 2 <= col < 6:
                            middle_control_BLACK += 1
                        if 2 <= row < 5 and (col < 2 or col > 5):
                            strategic_block_BLACK += 1
                        if piece.can_be_taken(self.board):
                            vulnerable_pieces_BLACK += 1

        # Adjust evaluation based on counts
        heuristic_value += (regular_pieces_RED * piece_weight) + (king_pieces_RED * king_weight)
        heuristic_value -= (regular_pieces_BLACK * piece_weight) + (king_pieces_BLACK * king_weight)

        # Back row advantage
        heuristic_value += (back_row_RED * back_row_weight) - (back_row_BLACK * back_row_weight)

        # Middle control
        heuristic_value += (middle_control_RED * middle_control_weight) - (middle_control_BLACK * middle_control_weight)

        # Strategic blocking
        heuristic_value += (strategic_block_RED * strategic_block_weight) - (strategic_block_BLACK * strategic_block_weight)

        # Vulnerable pieces
        heuristic_value -= (vulnerable_pieces_RED * vulnerable_pieces_weight) - (vulnerable_pieces_BLACK * vulnerable_pieces_weight)

        return heuristic_value


    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        offset_x = (800 - (SQUARE_SIZE * COLS)) // 2  # Same offset as squares

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win, x_offset=offset_x, y_offset=52)
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.BLACK_left -= 1
                else:
                    self.RED_left -= 1
    
    def winner(self):
        if self.BLACK_left <= 0 or not self.has_valid_moves(BLACK):
            time.sleep(2)
            return (f"RED wins!")

        elif self.RED_left <= 0 or not self.has_valid_moves(RED):
            time.sleep(2)
            return (f"BLACK wins!")
    

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def has_valid_moves(self, color):
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    if self.get_valid_moves(piece):
                        return True
    
        return False

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves