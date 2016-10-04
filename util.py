# Define some colors
BLACK = (0, 0, 0)  # background
LIGHT_RED = (153, 0, 0)  # empty squares
BLUE = (0, 102, 204)  # empty squares
GREEN = (0, 255, 0)  # PAWN
RED = (255, 0, 0)  # QUEEN
DARK_BLUE = (0, 0, 255)  # BISHOP
YELLOW = (255, 255, 0)  # ROOK
PURPLE = (128, 0, 128)  # KNIGHT
GREY = (192, 192, 192)  # highlighting
LIGHT_BLUE = (153, 204, 255)  # heaven
LIGHT_BLACK = (96, 96, 96)  # hell


# This sets the width and height of each grid location
SQUARE_WIDTH = 80
SQUARE_HEIGHT = 80

# This sets the margin between each Square
MARGIN = 8

# Dimensions of the board
BOARD_X = 4
BOARD_Y = 8

# Screen size
SIZE_X = SQUARE_WIDTH * BOARD_X + MARGIN * (BOARD_X + 1)
SIZE_Y = SQUARE_HEIGHT * (BOARD_Y + 2) + MARGIN * (BOARD_Y + 3)

# Grid offset
OFFSET = SQUARE_HEIGHT + MARGIN

# heaven (future board) height
HEAVEN_HEIGHT = 4

# piece offset
PIECE_OFFSET = 14
