"""
Piece class
"""

from abc import abstractmethod
from util import *


class Piece:
    name = ""
    alive = True
    enemy = False
    image = ""
    enemy_image = ""

    def __init__(self):
        pass

    @abstractmethod
    def get_moves(self, pos):
        pass

    def get_name(self):
        return self.name

    def get_image(self):
        if self.is_enemy():
            return self.enemy_image
        return self.image

    def is_alive(self):
        return self.alive

    def die(self):
        self.alive = False

    def is_enemy(self):
        return self.enemy

    def set_enemy(self):
        self.enemy = True

    @staticmethod
    def perpendicular_moves(pos):
        moves = []
        for x in range(BOARD_X):
            moves.append((x, pos[1]))
        for y in range(BOARD_Y):
            moves.append((pos[0], y))
        return moves

    @staticmethod
    def diagonal_moves(pos):
        moves = []
        for x in range(1, BOARD_X):
            if pos[0] + x < BOARD_X and pos[1] + x < BOARD_Y:
                moves.append((pos[0] + x, pos[1] + x))
            if pos[0] + x < BOARD_X and pos[1] - x >= 0:
                moves.append((pos[0] + x, pos[1] - x))
            if pos[0] - x >= 0 and pos[1] + x < BOARD_Y:
                moves.append((pos[0] - x, pos[1] + x))
            if pos[0] - x >= 0 and pos[1] - x >= 0:
                moves.append((pos[0] - x, pos[1] - x))
        return moves
