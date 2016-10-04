# Define some colors
BLACK = (0, 0, 0)  # background
WHITE = (255, 255, 255)  # empty squares
GREEN = (0, 255, 0)  # PAWN
RED = (255, 0, 0)  # QUEEN
BLUE = (0, 0, 255)  # BISHOP
YELLOW = (255, 255, 0)  # ROOK
PURPLE = (128, 0, 128)  # KNIGHT
GREY = (192, 192, 192)  # highlighting
LIGHT_BLUE = (153, 204, 255)  # heaven
DARK_RED = (153, 0, 0)  # hell


# This sets the width and height of each grid location
SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50

# This sets the margin between each Square
MARGIN = 5

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
