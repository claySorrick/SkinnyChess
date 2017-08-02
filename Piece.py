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

    @abstractmethod
    def get_attack_moves(self, pos):
        return self.get_moves(pos)

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
        final_moves = []
        for x in range(0, pos[0]):
            moves.append((x, pos[1]))
        if moves:
            final_moves.append(list(reversed(moves)))
            moves = []
        for x in range(pos[0]+1, BOARD_X):
            moves.append((x, pos[1]))
        if moves:
            final_moves.append(moves)
            moves = []
        for y in range(0, pos[1]):
            moves.append((pos[0], y))
        if moves:
            final_moves.append(list(reversed(moves)))
            moves = []
        for y in range(pos[1]+1, BOARD_Y):
            moves.append((pos[0], y))
        if moves:
            final_moves.append(moves)
        return final_moves

    @staticmethod
    def diagonal_moves(pos):
        moves1 = []
        moves2 = []
        moves3 = []
        moves4 = []
        final_moves = []
        for x in range(1, BOARD_X):
            if pos[0] + x < BOARD_X and pos[1] + x < BOARD_Y:
                moves1.append((pos[0] + x, pos[1] + x))
            if pos[0] + x < BOARD_X and pos[1] - x >= 0:
                moves2.append((pos[0] + x, pos[1] - x))
            if pos[0] - x >= 0 and pos[1] + x < BOARD_Y:
                moves3.append((pos[0] - x, pos[1] + x))
            if pos[0] - x >= 0 and pos[1] - x >= 0:
                moves4.append((pos[0] - x, pos[1] - x))
        if moves1:
            final_moves.append(moves1)
        if moves2:
            final_moves.append(moves2)
        if moves3:
            final_moves.append(moves3)
        if moves4:
            final_moves.append(moves4)
        return final_moves
