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
        self.targeted = []
        self.threatened = []
        self.player_pieces = []
        self.enemy_pieces = []
        self.sped_up = False
        self.init_board()

    def draw(self, screen, move_offset):
        if move_offset == 0:
            self.shift_board()
        screen.fill(BLACK)

        # draw board
        for x in range(self.col):
            for y in range(self.row):
                selected_mod = 1
                if self.board[x][y].is_selected():
                    selected_mod = 3
                elif self.board[x][y].is_targeted():
                    selected_mod = 3
                    pygame.draw.rect(screen, RED,
                                     [(MARGIN + SQUARE_WIDTH) * x + MARGIN + 1,
                                      (MARGIN + SQUARE_HEIGHT) * y + MARGIN + 1 + OFFSET + move_offset,
                                      SQUARE_WIDTH - 2,
                                      SQUARE_HEIGHT - 2])
                pygame.draw.rect(screen, self.board[x][y].get_color(),
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + (1 * selected_mod),
                                  (MARGIN + SQUARE_HEIGHT) * y + MARGIN + (1 * selected_mod) + OFFSET + move_offset,
                                  SQUARE_WIDTH - (2 * selected_mod),
                                  SQUARE_HEIGHT - (2 * selected_mod)])

        # draw heaven
        for x in range(self.col):
            for y in range(2):
                pygame.draw.rect(screen, self.heaven[x][y].get_color(),
                                 [(MARGIN + SQUARE_WIDTH) * x + MARGIN + 1,
                                  (MARGIN + SQUARE_HEIGHT) * (y - 1) + MARGIN + 1 + move_offset,
                                  SQUARE_WIDTH - 2,
                                  SQUARE_HEIGHT - 2])

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

        # draw heaven line
        pygame.draw.rect(screen, RED, [0, SQUARE_HEIGHT + MARGIN, SIZE_X, MARGIN])

        # draw hell line
        pygame.draw.rect(screen, RED, [0, (SQUARE_HEIGHT + MARGIN) * (BOARD_Y + 1), SIZE_X, MARGIN])

        # draw pieces last so they move over heaven/hell lines
        for x in range(self.col):
            for y in range(self.row):
                if y < self.heaven[x].__len__():
                    if self.heaven[x][y].has_piece():
                        screen.blit(self.heaven[x][y].get_piece().get_image(),
                                    ((MARGIN + SQUARE_WIDTH) * x + MARGIN + 1 + PIECE_OFFSET,
                                      (MARGIN + SQUARE_HEIGHT) * (y - 1) + MARGIN + 1 + move_offset + PIECE_OFFSET))
                if self.board[x][y].has_piece():
                    screen.blit(self.board[x][y].get_piece().get_image(),
                        ((MARGIN + SQUARE_WIDTH) * x + MARGIN + PIECE_OFFSET,
                        (MARGIN + SQUARE_HEIGHT) * y + MARGIN + OFFSET + move_offset + PIECE_OFFSET))

    def highlight_squares(self, squares):
        if squares:
            for path in squares:
                for x, y in path:
                    if self.board[x][y].highlight():
                        self.highlighted.append(self.board[x][y])
                    else:
                        break

    def unhighlight_squares(self):
        for sqr in self.highlighted:
            sqr.unhighlight()
        self.highlighted = []

    def target_squares(self, squares):
        if squares:
            for path in squares:
                for x, y in path:
                    if self.board[x][y].target():
                        self.targeted.append(self.board[x][y])
                        break
                    elif self.board[x][y].has_piece():
                        break

    def untarget_squares(self):
        for sqr in self.targeted:
            sqr.untarget()
        self.targeted = []

    def select(self, pos, scroll_offset):
        x = pos[0] // (SQUARE_WIDTH + MARGIN)
        y = (pos[1] - OFFSET - scroll_offset) // (SQUARE_HEIGHT + MARGIN)
        # click is off the board
        if x >= BOARD_X or x < 0 or y >= BOARD_Y or y < 0:
            return
        sqr = self.board[x][y]
        if sqr.is_selected():
            sqr.unselect()
            self.unselect()
            return
        if sqr in self.highlighted:
            # move piece
            sqr.set_piece(self.selected.get_piece())
            self.selected.remove_piece()
            self.unselect()
            self.enemy_attack()
        elif sqr in self.targeted:
            # take piece
            self.take_piece(self.selected, sqr)
            self.unselect()
            self.enemy_attack()
        else:
            sqr.select()
            self.unhighlight_squares()
            self.untarget_squares()
            if self.selected and self.selected != sqr:
                self.selected.unselect()
            self.selected = sqr
            if sqr.has_player_piece():
                piece = sqr.get_piece()
                moves = piece.get_moves([x, y])
                self.highlight_squares(moves)
                attacks = piece.get_attack_moves([x, y])
                self.target_squares(attacks)

    def unselect(self):
        if self.selected:
            self.selected.unselect()
        self.selected = []
        self.unhighlight_squares()
        self.untarget_squares()

    def shift_board(self):
        # move bottom to hell
        for x in range(BOARD_X):
            if self.board[x][-1].is_selected():
                self.board[x][-1].unselect()
                self.unhighlight_squares()
            if self.board[x][-1].has_player_piece():
                self.player_pieces.remove(self.board[x][-1].get_piece())
            elif self.board[x][-1].has_enemy_piece():
                self.enemy_pieces.remove(self.board[x][-1].get_piece())
            self.hell[x].insert(0, self.board[x].pop())

        # move heaven into board
        for x in range(BOARD_X):
            rand = random.randint(0, 1000)
            new_square = Square()
            if rand % 2 == 0:
                new_square.set_enemy_piece(self.get_random_piece())
            new_square.set_board_color(self.board[x][1].get_board_color())
            if self.heaven[x][-1].has_enemy_piece():
                self.enemy_pieces.append(self.heaven[x][-1].get_piece())
            self.board[x].insert(0, self.heaven[x].pop())
            self.heaven[x].insert(0, new_square)

    def take_piece(self, attacker, victim):
        piece = attacker.get_piece()
        if victim.has_enemy_piece():
            self.enemy_pieces.remove(victim.get_piece())
        else:
            self.player_pieces.remove(victim.get_piece())
        victim.set_piece(piece)
        attacker.remove_piece()

    def enemy_attack(self):
        for x in range(BOARD_X):
            for y in range(BOARD_Y):
                attacker = self.board[x][y]
                if attacker.has_enemy_piece():
                    attack_moves = attacker.get_piece().get_attack_moves([x, y])
                    for attack in attack_moves:
                        for xx, yy in attack:
                            if self.board[xx][yy].has_player_piece():
                                self.take_piece(attacker, self.board[xx][yy])
                                print("tooken")
                                break
                            else:
                                break

                else:
                    continue


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

    def is_valid(self):
        if self.player_pieces:
            return True
        return False

    def init_board(self):
        # Players pieces
        self.board[0][6].set_piece(Rook())
        self.player_pieces.append(self.board[0][6].get_piece())
        self.board[1][6].set_piece(Knight())
        self.player_pieces.append(self.board[1][6].get_piece())
        self.board[2][6].set_piece(Bishop())
        self.player_pieces.append(self.board[2][6].get_piece())
        self.board[3][6].set_piece(Queen())
        self.player_pieces.append(self.board[3][6].get_piece())
        self.board[1][5].set_piece(Pawn())
        self.player_pieces.append(self.board[1][5].get_piece())
        self.board[2][5].set_piece(Pawn())
        self.player_pieces.append(self.board[2][5].get_piece())
        # enemy pieces
        # self.board[0][0].set_enemy_piece(Rook())
        # self.enemy_pieces.append(self.board[0][0].get_piece())
        self.board[1][0].set_enemy_piece(Knight())
        self.enemy_pieces.append(self.board[1][0].get_piece())
        self.board[2][0].set_enemy_piece(Bishop())
        self.enemy_pieces.append(self.board[2][0].get_piece())
        # self.board[3][0].set_enemy_piece(Queen())
        # self.enemy_pieces.append(self.board[3][0].get_piece())
        self.board[1][1].set_enemy_piece(Pawn())
        self.enemy_pieces.append(self.board[1][1].get_piece())
        self.board[2][1].set_enemy_piece(Pawn())
        self.enemy_pieces.append(self.board[2][1].get_piece())

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
