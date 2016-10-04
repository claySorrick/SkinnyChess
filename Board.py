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
        self.selected = ""
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
                if self.board[x][y].is_selected():
                    selected_mod = 3
                if self.board[x][y].is_highlighted():
                    color = GREY
                else:
                    if (x + y) % 2 == 0:
                        color = BLUE
                    else:
                        color = LIGHT_BLACK

                pygame.draw.rect(screen, color,
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
            for y in range(-1, 1):
                pygame.draw.rect(screen, LIGHT_BLUE,
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + 1,
                                  (MARGIN + SQUARE_HEIGHT) * y + MARGIN + 1 + move_offset,
                                  SQUARE_WIDTH - 2,
                                  SQUARE_HEIGHT - 2])

        # draw hell
        for x in range(self.col):
            pygame.draw.rect(screen, LIGHT_RED,
                             [(MARGIN + SQUARE_WIDTH) * x + MARGIN + 1,
                              (MARGIN + SQUARE_HEIGHT) * (BOARD_Y + 1) + MARGIN + 1 + move_offset,
                              SQUARE_WIDTH - 2,
                              SQUARE_HEIGHT - 2])

    def highlight_squares(self, squares):
        if squares:
            for x, y in squares:
                self.board[x][y].highlight()
                self.highlighted.append(self.board[x][y])

    def unhighlight_squares(self):
        for sqr in self.highlighted:
            sqr.unhighlight()
        self.highlighted = []

    def select(self, pos, scroll_offset):
        x = pos[0] // (SQUARE_WIDTH + MARGIN)
        y = (pos[1] - OFFSET - scroll_offset) // (SQUARE_HEIGHT + MARGIN)
        print(x, y)
        if x >= BOARD_X or x < 0 or y >= BOARD_Y or y < 0:
            return
        sqr = self.board[x][y]
        if sqr.is_selected():
            sqr.unselect()
            self.selected = ""
            self.unhighlight_squares()
            return
        if self.highlighted.__contains__(sqr):
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
            new_piece = ""
        elif rand < 70:
            new_piece = Knight()
        elif rand < 80:
            new_piece = Bishop()
        else:
            new_piece = Pawn()
        return new_piece
