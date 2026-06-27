"""

This file contains the Food class

"""

import random
import pygame
from settings import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, RED


class Food:
    def __init__(self, occupied_positions):
        self.position = self.random_position(occupied_positions)

    def random_position(self, occupied_positions):
        """
        Choose a random position that is not inside any snake
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)

            if position not in occupied_positions:
                return position

    def move_to_new_position(self, occupied_positions):
        """
        Move food after one of the snakes eats it
        """
        self.position = self.random_position(occupied_positions)

    def draw(self, screen):
        """
        Draw the food on the screen
        """
        x, y = self.position

        rectangle = pygame.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )

        pygame.draw.rect(screen, RED, rectangle)
