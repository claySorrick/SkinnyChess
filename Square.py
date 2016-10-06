"""
Square class
"""

from util import *


class Square:

    def __init__(self):
        self.color = GREY
        self.board_color = ""
        self.piece = ""
        self.selected = False
        self.highlighted = False

    def get_board_color(self):
        return self.board_color

    def set_board_color(self, color):
        self.board_color = color
        self.color = color

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def set_enemy_piece(self, piece):
        if piece:
            piece.set_enemy()
            self.piece = piece

    def remove_piece(self):
        self.piece = ""

    def has_piece(self):
        if not self.piece:
            return False
        return True

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def highlight(self):
        if not self.has_piece():
            self.highlighted = True
            self.color = BLUE
            return True
        return False

    def unhighlight(self):
        self.highlighted = False
        self.color = self.board_color

    def is_highlighted(self):
        return self.highlighted
