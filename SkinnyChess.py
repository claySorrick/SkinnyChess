"""
Skinny Chess
a game with similarities to chess
the board is 4x8 and moves downward out of view
the player begins with 8 chess pieces: 4xPAWN 1xROOK 1xKNIGHT 1xBISHOP 1xQUEEN
player must move them up freely, following their move rules
enemy pieces begin to appear on the board ahead
enemy pieces only move if they can attack a player piece
player must use piece move rules to their advantage when taking an enemy piece
player pieces may only be removed from play when taken by an enemy piece or fall below the kill line
the kill line is the bottom of the 4x8 board
if a piece falls below the kill line, the piece is removed
player loses when all player pieces are removed
endless game, player gains points based on length of survival
"""
import pygame

from Board import Board
from util import *

# Initialize pygame
pygame.init()

# Set the height and width of the screen
size = [SIZE_X, SIZE_Y]
screen = pygame.display.set_mode(size)

board = Board(BOARD_X, BOARD_Y)

# Set title of screen
pygame.display.set_caption("Skinny Chess 1.0")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
clk_counter = 0
scroll_offset = 2

# -------- Main Program Loop -----------
while not done:

    if scroll_offset == 0:
        scroll_offset = 1

    # Increment board movement offset
    clk_counter += 1
    if clk_counter % 10 == 0:
        clk_counter = 0
        scroll_offset += 2
        if scroll_offset > OFFSET:
            scroll_offset = 0

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.select(pygame.mouse.get_pos(), scroll_offset)

            # print("Click ", pygame.mouse.get_pos())

    # Draw the grid
    board.draw(screen, scroll_offset)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
