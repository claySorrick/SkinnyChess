"""
Piece classes
"""

from Piece import Piece
from util import *
import pygame

"""
Pawn Piece class
"""


class Pawn(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.name = "PAWN"
        self.enemy = False
        self.alive = True
        self.image = pygame.image.load("./images/pw.png")
        self.enemy_image = pygame.image.load("./images/pb.png")

    def get_moves(self, pos):
        x = pos[0]
        y = pos[1]
        moves = []
        if 0 < y < BOARD_Y:
            if self.enemy:
                moves = [(x, y + 1)]
            else:
                moves = [(x, y - 1)]
        return moves

    def get_attack_moves(self, pos):
        x = pos[1]
        y = pos[2]
        attacks = []
        if 0 < y < BOARD_Y and 0 < x < BOARD_X:
            if self.enemy:
                attacks = [(x + 1, y + 1), (x - 1, y + 1)]
            else:
                attacks = [(x + 1, y - 1), (x - 1, y - 1)]
        return attacks


"""
Rook Piece class
"""


class Rook(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.name = "ROOK"
        self.enemy = False
        self.alive = True
        self.image = pygame.image.load("./images/rw.png")
        self.enemy_image = pygame.image.load("./images/rb.png")

    def get_moves(self, pos):
        return Piece.perpendicular_moves(pos)


"""
Bishop Piece class
"""


class Bishop(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.name = "BISHOP"
        self.enemy = False
        self.alive = True
        self.image = pygame.image.load("./images/bw.png")
        self.enemy_image = pygame.image.load("./images/bb.png")

    def get_moves(self, pos):
        return Piece.diagonal_moves(pos)


"""
Queen Piece class
"""


class Queen(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.name = "QUEEN"
        self.enemy = False
        self.alive = True
        self.image = pygame.image.load("./images/qw.png")
        self.enemy_image = pygame.image.load("./images/qb.png")

    def get_moves(self, pos):
        return Piece.diagonal_moves(pos) + Piece.perpendicular_moves(pos)


"""
Knight Piece class
"""


class Knight(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.name = "KNIGHT"
        self.enemy = False
        self.alive = True
        self.image = pygame.image.load("./images/hw.png")
        self.enemy_image = pygame.image.load("./images/hb.png")

    def get_moves(self, pos):
        moves = []
        if pos[0] + 2 < BOARD_X and pos[1] + 1 < BOARD_Y:
            moves.append((pos[0] + 2, pos[1] + 1))
        if pos[0] + 2 < BOARD_X and pos[1] - 1 >= 0:
            moves.append((pos[0] + 2, pos[1] - 1))
        if pos[0] + 1 < BOARD_X and pos[1] + 2 < BOARD_Y:
            moves.append((pos[0] + 1, pos[1] + 2))
        if pos[0] - 1 >= 0 and pos[1] + 2 < BOARD_Y:
            moves.append((pos[0] - 1, pos[1] + 2))
        if pos[0] - 2 >= 0 and pos[1] - 1 >= 0:
            moves.append((pos[0] - 2, pos[1] - 1))
        if pos[0] - 2 >= 0 and pos[1] + 1 < BOARD_Y:
            moves.append((pos[0] - 2, pos[1] + 1))
        if pos[0] - 1 >= 0 and pos[1] - 2 >= 0:
            moves.append((pos[0] - 1, pos[1] - 2))
        if pos[0] + 1 < BOARD_X and pos[1] - 2 >= 0:
            moves.append((pos[0] + 1, pos[1] - 2))
        return moves
