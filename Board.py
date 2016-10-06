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
        self.selected = ""
        self.highlighted = []
        self.init_board()

    def draw(self, screen, move_offset):
        if move_offset == 0:
            print("shifting board")
            self.shift_board()
        screen.fill(BLACK)

        # draw board
        for x in range(self.col):
            for y in range(self.row):
                selected_mod = 1
                if self.board[x][y].is_selected():
                    selected_mod = 3
                pygame.draw.rect(screen, self.board[x][y].get_color(),
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + (1 * selected_mod),
                                  (MARGIN + SQUARE_HEIGHT) * y + MARGIN + (1 * selected_mod) + OFFSET + move_offset,
                                  SQUARE_WIDTH - (2 * selected_mod),
                                  SQUARE_HEIGHT - (2 * selected_mod)])
                if self.board[x][y].has_piece():
                    screen.blit(self.board[x][y].get_piece().get_image(),
                        ((MARGIN + SQUARE_WIDTH) * x + MARGIN + (1 * selected_mod) + PIECE_OFFSET,
                        (MARGIN + SQUARE_HEIGHT) * y + MARGIN + (1 * selected_mod) + OFFSET + move_offset + PIECE_OFFSET))

        # draw heaven
        for x in range(self.col):
            for y in range(2):
                pygame.draw.rect(screen, self.heaven[x][y].get_color(),
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + 1,
                                  (MARGIN + SQUARE_HEIGHT) * (y - 1) + MARGIN + 1 + move_offset,
                                  SQUARE_WIDTH - 2,
                                  SQUARE_HEIGHT - 2])
                if self.heaven[x][y].has_piece():
                    screen.blit(self.heaven[x][y].get_piece().get_image(),
                                ((MARGIN + SQUARE_WIDTH) * x + MARGIN + 1 + PIECE_OFFSET,
                                  (MARGIN + SQUARE_HEIGHT) * (y - 1) + MARGIN + 1 + move_offset + PIECE_OFFSET))

        # draw hell
        for x in range(self.col):
            y = 0
            pygame.draw.rect(screen, self.hell[x][y].get_color(),
                             [(MARGIN + SQUARE_WIDTH) * x + MARGIN + 1,
                              (MARGIN + SQUARE_HEIGHT) * (BOARD_Y + 1) + MARGIN + 1 + move_offset,
                              SQUARE_WIDTH - 2,
                              SQUARE_HEIGHT - 2])
            if self.hell[x][y].has_piece():
                screen.blit(self.hell[x][y].get_piece().get_image(),
                            ((MARGIN + SQUARE_WIDTH) * x + MARGIN + 1 + PIECE_OFFSET,
                              (MARGIN + SQUARE_HEIGHT) * (BOARD_Y + 1) + MARGIN + 1 + move_offset + PIECE_OFFSET))

    def highlight_squares(self, squares):
        if squares:
            for x, y in squares:
                if self.board[x][y].highlight():
                    self.highlighted.append(self.board[x][y])

    def unhighlight_squares(self):
        for sqr in self.highlighted:
            sqr.unhighlight()
        self.highlighted = []

    def select(self, pos, scroll_offset):
        x = pos[0] // (SQUARE_WIDTH + MARGIN)
        y = (pos[1] - OFFSET - scroll_offset) // (SQUARE_HEIGHT + MARGIN)
        print(x, y)
        # click is off the board
        if x >= BOARD_X or x < 0 or y >= BOARD_Y or y < 0:
            return
        sqr = self.board[x][y]
        if sqr.is_selected():
            sqr.unselect()
            self.selected = ""
            self.unhighlight_squares()
            return
        if sqr in self.highlighted:
            sqr.set_piece(self.selected.get_piece())
            self.selected.remove_piece()
            self.selected.unselect()
            self.selected = []
            self.unhighlight_squares()
        else:
            sqr.select()
            self.unhighlight_squares()
            if self.selected and self.selected != sqr:
                self.selected.unselect()
            self.selected = sqr
            if sqr.has_piece():
                piece = sqr.get_piece()
                moves = piece.get_moves([x, y])
                self.highlight_squares(moves)

    def shift_board(self):
        # move bottom to hell
        for x in range(BOARD_X):
            self.hell[x].insert(0, self.board[x].pop())

        # move heaven into board
        for x in range(BOARD_X):
            rand = random.randint(0, 2)
            new_square = Square()
            if rand == 0:
                new_square.set_enemy_piece(self.get_random_piece())
            new_square.set_board_color(self.board[x][1].get_board_color())
            self.board[x].insert(0, self.heaven[x].pop())

            self.heaven[x].insert(0, new_square)

    @staticmethod
    def get_random_piece():
        rand = random.randint(0, 100)
        if rand < 60:
            new_piece = ""
        elif rand < 70:
            new_piece = Knight()
        elif rand < 80:
            new_piece = Bishop()
        else:
            new_piece = Pawn()
        return new_piece

    def init_board(self):
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

        # board
        for x in range(self.col):
            for y in range(self.row):
                # draw grey and light black squares
                if (x + y) % 2 == 0:
                    self.board[x][y].set_board_color(GREY)
                else:
                    self.board[x][y].set_board_color(LIGHT_BLACK)

        # heaven
        for x in range(self.col):
            for y in range(HEAVEN_HEIGHT):
                # draw grey and light black squares
                if (x + y) % 2 == 0:
                    self.heaven[x][y].set_board_color(GREY)
                else:
                    self.heaven[x][y].set_board_color(LIGHT_BLACK)

        # hell
        for x in range(self.col):
            for y in range(1):
                # draw grey and light black squares
                if (x + y) % 2 == 0:
                    self.hell[x][y].set_board_color(GREY)
                else:
                    self.hell[x][y].set_board_color(LIGHT_BLACK)
