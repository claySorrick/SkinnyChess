"""
Board Class
"""

from Square import Square
from Pieces import *
from util import *
import pygame
import random


class Board:
    def __init__(self, col, row):
        self.board = [[Square() for c in range(row)] for c in range(col)]
        self.heaven = [[Square() for c in range(HEAVEN_HEIGHT)] for c in range(col)]
        self.hell = [[Square()] for c in range(col)]
        self.row = row
        self.col = col
        # Players pieces
        self.board[0][7].set_piece(Rook())
        self.board[1][7].set_piece(Knight())
        self.board[2][7].set_piece(Bishop())
        self.board[3][7].set_piece(Queen())
        self.board[1][6].set_piece(Pawn())
        self.board[2][6].set_piece(Pawn())
        # enemy pieces
        self.board[0][0].set_enemy_piece(Rook())
        self.board[1][0].set_enemy_piece(Knight())
        self.board[2][0].set_enemy_piece(Bishop())
        self.board[3][0].set_enemy_piece(Queen())
        self.board[1][1].set_enemy_piece(Pawn())
        self.board[2][1].set_enemy_piece(Pawn())
        # initial heaven
        self.heaven[0][HEAVEN_HEIGHT-1].set_enemy_piece(Pawn())
        self.heaven[1][HEAVEN_HEIGHT-2].set_enemy_piece(Knight())
        self.selected = [0, 0]
        self.highlighted = []

    def draw(self, screen, move_offset):
        if move_offset == 0:
            print("shifting board")
            self.shift_board()
        screen.fill(BLACK)

        # draw board
        for x in range(self.col):
            for y in range(self.row):
                selected_mod = 1
                color = self.piece_color(self.board[x][y].get_piece())
                if self.board[x][y].is_highlighted():
                    color = GREY
                if self.board[x][y].is_selected():
                    selected_mod = 3

                pygame.draw.rect(screen, color,
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + (1 * selected_mod),
                                  (MARGIN + SQUARE_HEIGHT) * y + MARGIN + (1 * selected_mod) + OFFSET + move_offset,
                                  SQUARE_WIDTH - (2 * selected_mod),
                                  SQUARE_HEIGHT - (2 * selected_mod)])
        selected_mod = 1

        # draw heaven
        for x in range(self.col):
            for y in range(-1, 1):
                pygame.draw.rect(screen, LIGHT_BLUE,
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + (1 * selected_mod),
                                  (MARGIN + SQUARE_HEIGHT) * y + MARGIN + (1 * selected_mod) + move_offset,
                                  SQUARE_WIDTH - (2 * selected_mod),
                                  SQUARE_HEIGHT - (2 * selected_mod)])

        # draw hell
        for x in range(self.col):
            pygame.draw.rect(screen, DARK_RED,
                             [(MARGIN + SQUARE_WIDTH) * x + MARGIN + (1 * selected_mod),
                              (MARGIN + SQUARE_HEIGHT) * (BOARD_Y + 1) + MARGIN + (1 * selected_mod) + move_offset,
                              SQUARE_WIDTH - (2 * selected_mod),
                              SQUARE_HEIGHT - (2 * selected_mod)])

    @staticmethod
    def piece_color(piece):
        if isinstance(piece, Pawn):
            color = GREEN
        elif isinstance(piece, Queen):
            color = RED
        elif isinstance(piece, Bishop):
            color = BLUE
        elif isinstance(piece, Rook):
            color = YELLOW
        elif isinstance(piece, Knight):
            color = PURPLE
        else:
            color = WHITE
        return color

    def highlight(self, squares):
        if squares:
            for x, y in squares:
                if not self.board[x][y].has_piece():
                    self.board[x][y].highlight()
                    self.highlighted.append((x, y))

    def unhighlight(self):
        for x, y in self.highlighted:
            self.board[x][y].unhighlight()
        self.highlighted = []

    def select(self, pos, scroll_offset):
        x = pos[0] // (SQUARE_WIDTH + MARGIN)
        y = (pos[1] - OFFSET - scroll_offset) // (SQUARE_HEIGHT + MARGIN)
        print(x, y)
        if x >= BOARD_X or x < 0 or y >= BOARD_Y or y < 0:
            return
        if self.selected and x == self.selected[0] and y == self.selected[1]:
            self.board[x][y].unselect()
            self.selected = []
            self.unhighlight()
            return
        if self.highlighted.__contains__((x, y)):
            self.board[x][y].set_piece(self.board[self.selected[0]][self.selected[1]].get_piece())
            self.board[self.selected[0]][self.selected[1]].remove_piece()
            self.board[self.selected[0]][self.selected[1]].unselect()
            self.selected = []
            self.unhighlight()
        else:
            self.board[x][y].select()
            self.unhighlight()
            if self.selected and self.selected != [x, y]:
                self.board[self.selected[0]][self.selected[1]].unselect()
            self.selected = [x, y]
            if self.board[x][y].has_piece():
                piece = self.board[x][y].get_piece()
                print(piece.is_enemy())
                moves = piece.get_moves([x, y])
                self.highlight(moves)

    def shift_board(self):
        # move bottom to hell
        for x in range(BOARD_X):
            self.hell[x].insert(x, self.board[x].pop())

        # move heaven into board
        for x in range(BOARD_X):
            self.board[x].insert(0, self.heaven[x].pop())
            rand = random.randint(0, 2)
            new_square = Square()
            if rand == 0:
                new_square.set_enemy_piece(self.get_random_piece())
            self.heaven[x].insert(0, new_square)

        # # move selected and highlighted squares when shifting
        # if self.selected:
        #     # self.board[self.selected[0]][self.selected[1]].unselect()
        #     self.selected[1] += 1

    @staticmethod
    def get_random_piece():
        rand = random.randint(0, 100)
        if rand < 60:
            new_piece = Piece()
        elif rand < 70:
            new_piece = Knight()
        elif rand < 80:
            new_piece = Bishop()
        else:
            new_piece = Pawn()
        return new_piece