"""

This file contains the Game class.

"""

import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    START_SPEED,
    MAX_SPEED,
    POINTS_ADVANTAGE_TO_WIN,
    BLACK,
    WHITE,
    GREEN,
    BLUE,
    DARK_GRAY,
    GRID_WIDTH,
    GRID_HEIGHT,
    AI_MOVE_EVERY,
    CELL_SIZE,
    PURPLE,
    PLAYER_HEAD_COLOR,
    AI_HEAD_COLOR,
)
from snake import Snake
from food import Food


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game: Player vs AI")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.reset()

    def draw_snake_intersections(self):
        """
        Overlap
        """
        player_positions = set(self.player_snake.body)
        ai_positions = set(self.ai_snake.body)

        intersection_positions = player_positions.intersection(ai_positions)

        for x, y in intersection_positions:
            rectangle = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(self.screen, PURPLE, rectangle)


    def reset(self):
        """
        New game
        """

        self.ai_move_counter = 0

        self.player_snake = Snake(
            body=[(5, 10), (4, 10), (3, 10)],
            direction="RIGHT",
            color=GREEN,
            head_color=PLAYER_HEAD_COLOR,
        )

        self.ai_snake = Snake(
            body=[(24, 10), (25, 10), (26, 10)],
            direction="LEFT",
            color=BLUE,
            head_color=AI_HEAD_COLOR,
        )

        self.food = Food(self.all_snake_positions())

        self.player_score = 0
        self.ai_score = 0

        self.game_over = False
        self.end_message = ""

    def all_snake_positions(self):
        """
        Return all cells currently occupied by both snakes
        Used so food does not spawn inside a snake
        """
        return self.player_snake.body + self.ai_snake.body

    def handle_events(self):
        """
        Read keyboard and events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    self.handle_movement_keys(event.key)
                else:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False

        return True

    def handle_movement_keys(self, key):
        """
        Keyboard events
        """
        if key == pygame.K_UP:
            self.player_snake.change_direction("UP")
        elif key == pygame.K_DOWN:
            self.player_snake.change_direction("DOWN")
        elif key == pygame.K_LEFT:
            self.player_snake.change_direction("LEFT")
        elif key == pygame.K_RIGHT:
            self.player_snake.change_direction("RIGHT")

    def choose_ai_direction(self):
        """
        AI
        """
        possible_directions = ["UP", "DOWN", "LEFT", "RIGHT"]

        safe_directions = []

        for direction in possible_directions:
            if self.is_backwards_move(self.ai_snake, direction):
                continue

            new_head = self.ai_snake.next_head_position(direction)

            if self.position_hits_body(new_head, self.ai_snake.body):
                continue

            safe_directions.append(direction)

        # If there are no safe moves, just keep moving
        if not safe_directions:
            return self.ai_snake.direction

        # Choose the safe move that gets closest to the food
        best_direction = safe_directions[0]
        best_distance = self.distance_to_food(
            self.ai_snake.next_head_position(best_direction)
        )

        for direction in safe_directions:
            new_head = self.ai_snake.next_head_position(direction)
            distance = self.distance_to_food(new_head)

            if distance < best_distance:
                best_distance = distance
                best_direction = direction

        return best_direction

    def is_backwards_move(self, snake, new_direction):
        """
        Return True if new_direction is the opposite of the snake's current direction.
        """
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }

        return new_direction == opposites[snake.direction]

    def position_hits_body(self, position, body):
        """
        Return True if a position is inside a snake body
        """
        return position in body

    def distance_to_food(self, position):
        """
        Calculate distance from a position to the food.

        """
        x, y = position
        food_x, food_y = self.food.position

        normal_x_distance = abs(x - food_x)
        normal_y_distance = abs(y - food_y)

        wrap_x_distance = GRID_WIDTH - normal_x_distance
        wrap_y_distance = GRID_HEIGHT - normal_y_distance

        shortest_x_distance = min(normal_x_distance, wrap_x_distance)
        shortest_y_distance = min(normal_y_distance, wrap_y_distance)

        return shortest_x_distance + shortest_y_distance

    def update(self):
        """
        Game clock

        """
        if self.game_over:
            return

        # Player moves every update
        self.player_snake.move()

        # AI moves only every few updates
        self.ai_move_counter += 1

        if self.ai_move_counter >= AI_MOVE_EVERY:
            ai_direction = self.choose_ai_direction()
            self.ai_snake.change_direction(ai_direction)
            self.ai_snake.move()

            self.ai_move_counter = 0

        # Check if player ate the food.
        if self.player_snake.head_position() == self.food.position:
            self.player_score += 1
            self.player_snake.grow()
            self.food.move_to_new_position(self.all_snake_positions())

        # Check if AI ate the food.
        if self.ai_snake.head_position() == self.food.position:
            self.ai_score += 1
            self.ai_snake.grow()
            self.food.move_to_new_position(self.all_snake_positions())


        if self.player_snake.hits_itself():
            self.game_over = True
            self.end_message = "You lost!"

        #if self.ai_snake.hits_itself():
        #    self.game_over = True
        #    self.end_message = "AI crashed. You win!"

        # Check 15-point advantage win/lose condition
        score_difference = self.player_score - self.ai_score

        if score_difference >= POINTS_ADVANTAGE_TO_WIN:
            self.game_over = True
            self.end_message = "You win by 15 points!"

        if score_difference <= -POINTS_ADVANTAGE_TO_WIN:
            self.game_over = True
            self.end_message = "AI wins by 15 points!"

    def current_speed(self):
        """
        Increase speed only when the player is winning

        """
        advantage = self.player_score - self.ai_score

        if advantage <= 0:
            return START_SPEED

        speed = START_SPEED + advantage // 3
        return min(speed, MAX_SPEED)

    def draw_text(self, text, x, y):
        """
        Draw text on the screen
        """
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x, y))

    def draw(self):
        """
        Draw everything on the screen
        """
        self.screen.fill(BLACK)

        self.player_snake.draw(self.screen)
        self.ai_snake.draw(self.screen)

        # Overlap
        self.draw_snake_intersections()

        self.food.draw(self.screen)

        self.draw_text(f"Player: {self.player_score}", 10, 10)
        self.draw_text(f"AI: {self.ai_score}", 10, 40)

        advantage = self.player_score - self.ai_score
        self.draw_text(f"Advantage: {advantage}", 10, 70)

        if self.game_over:
            self.draw_game_over_screen()

        pygame.display.update()

    def draw_game_over_screen(self):
        """
        Draw the game over message.
        """
        rectangle = pygame.Rect(70, 120, SCREEN_WIDTH - 140, 170)
        pygame.draw.rect(self.screen, DARK_GRAY, rectangle)

        self.draw_text(self.end_message, 150, 145)
        self.draw_text(f"Player: {self.player_score}", 200, 180)
        self.draw_text(f"AI: {self.ai_score}", 235, 215)
        self.draw_text("Press R to restart", 180, 250)
        self.draw_text("Press Q to quit", 200, 280)

    def run(self):
        """
        Main game loop
        """
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(self.current_speed())

        pygame.quit()
