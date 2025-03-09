from .constants import BLACK, RED, SQUARE_SIZE, GREY, CROWN, BLUE
import pygame

class Piece:
    PADDING = 15

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 #since I want piece to be in middle of square
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    
    def draw(self, win, x_offset=0, y_offset=0):
        radius = (SQUARE_SIZE // 2) - 10
        pygame.draw.circle(win, self.color, (self.x + x_offset, self.y + y_offset), radius)
        if self.king:
            win.blit(CROWN, (self.x + x_offset - CROWN.get_width()//2, self.y + y_offset - CROWN.get_height()//2))
            
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self): #for internal representation whivh will help with debugging
        return str(self.color)
    
    def can_be_taken(self, board):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Possible directions for taking a piece
        for direction in directions:
            row, col = self.row + direction[0], self.col + direction[1]
            if 0 <= row < len(board) and 0 <= col < len(board[0]):
                if board[row][col] != 0 and board[row][col].color != self.color:
                    # Check if the piece can be taken by jumping over it
                    jump_row, jump_col = row + direction[0], col + direction[1]
                    if 0 <= jump_row < len(board) and 0 <= jump_col < len(board[0]):
                        if board[jump_row][jump_col] == 0:
                            return True
        return False