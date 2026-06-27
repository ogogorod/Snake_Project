"""

This file contains the Snake class

"""

import pygame
from settings import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, GREEN


class Snake:
    def __init__(self, body=None, direction="RIGHT", color=GREEN, head_color=None):
        """
        Create a snake

        """

        if body is None:
            self.body = [(5, 10), (4, 10), (3, 10)]
        else:
            self.body = body

        self.direction = direction
        self.color = color
        self.needs_to_grow = False
        self.head_color = head_color if head_color is not None else color

    def change_direction(self, new_direction):
        """
        Change the snake direction
        """
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }

        if new_direction != opposites[self.direction]:
            self.direction = new_direction

    def next_head_position(self, direction=None):
        """
        Return where the snake head would be after one move

        """
        if direction is None:
            direction = self.direction

        head_x, head_y = self.body[0]

        if direction == "UP":
            new_head = (head_x, head_y - 1)
        elif direction == "DOWN":
            new_head = (head_x, head_y + 1)
        elif direction == "LEFT":
            new_head = (head_x - 1, head_y)
        else:  # RIGHT
            new_head = (head_x + 1, head_y)

        new_x, new_y = new_head

        # Wrap around the board
        new_x = new_x % GRID_WIDTH
        new_y = new_y % GRID_HEIGHT

        return (new_x, new_y)

    def move(self):
        """
        Move the snake one cell forward
        """
        new_head = self.next_head_position()

        # Add the new head at the front of the body.
        self.body.insert(0, new_head)

        # If the snake ate food, it grows and we do not remove the tail.
        if self.needs_to_grow:
            self.needs_to_grow = False
        else:
            self.body.pop()

    def grow(self):
        """
        Tell the snake to grow on the next move
        """
        self.needs_to_grow = True

    def head_position(self):
        """
        Return the position of the snake head
        """
        return self.body[0]

    def hits_wall(self):
        """
        Return False because walls are traversable
        """
        return False

    def hits_itself(self):
        """
        Return True if the snake head touches its own body
        """
        head = self.head_position()
        body_without_head = self.body[1:]

        return head in body_without_head

    def draw(self, screen):
        """
        Draw the snake

        """
        for index, (x, y) in enumerate(self.body):
            rectangle = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            if index == 0:
                pygame.draw.rect(screen, self.head_color, rectangle)
            else:
                pygame.draw.rect(screen, self.color, rectangle)
