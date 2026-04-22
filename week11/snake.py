import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)
colorPURPLE = (160, 32, 240)

# Font for text
font = pygame.font.SysFont("Verdana", 20)

# Draw grid
def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (j * CELL, i * CELL, CELL, CELL), 1)

# Point class for coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Snake class
class Snake:
    def __init__(self):
        # Snake body as list of points
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]

        # Initial moving direction
        self.dx = 0
        self.dy = -1

        # Player score
        self.score = 0

    def move(self):
        # Move snake body from tail to head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Move snake head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Teleport through borders
        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1

    def draw(self):
        # Draw snake head
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        # Draw snake body
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]

        # If snake eats food
        if head.x == food.pos.x and head.y == food.pos.y:
            # Increase snake body by one segment
            self.body.append(Point(self.body[-1].x, self.body[-1].y))

            # Add food weight to score
            self.score += food.weight

            # Generate new food after eating
            food.generate_random_pos(self.body)

    def check_self_collision(self):
        head = self.body[0]

        # Check collision with itself
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

# Food class
class Food:
    def __init__(self):
        self.pos = Point(9, 9)

        # Food can have different weights
        self.weight = 1

        # Food has limited lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000  # milliseconds = 5 seconds

        # Set initial random properties
        self.randomize_food()

    def randomize_food(self):
        # Randomly choose food weight
        self.weight = random.choice([1, 2, 3])

        # Set different color depending on weight
        if self.weight == 1:
            self.color = colorGREEN
        elif self.weight == 2:
            self.color = colorBLUE
        else:
            self.color = colorPURPLE

        # Reset timer when new food appears
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        # Draw food
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

        # Show weight number on food
        text = font.render(str(self.weight), True, colorWHITE)
        screen.blit(text, (self.pos.x * CELL + 8, self.pos.y * CELL + 4))

    def generate_random_pos(self, snake_body):
        # Randomize food type every time it respawns
        self.randomize_food()

        # Find free position not inside snake
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            inside_snake = False
            for segment in snake_body:
                if segment.x == x and segment.y == y:
                    inside_snake = True
                    break

            if not inside_snake:
                self.pos.x = x
                self.pos.y = y
                break

    def is_expired(self):
        # Check if food lifetime is over
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.lifetime

# Show score
def show_score(score):
    text = font.render(f"Score: {score}", True, colorWHITE)
    screen.blit(text, (10, 10))

# Show current food weight
def show_food_info(food):
    text = font.render(f"Food weight: {food.weight}", True, colorWHITE)
    screen.blit(text, (10, 40))

# Game over screen
def game_over():
    screen.fill(colorBLACK)
    over_text = font.render("Game Over", True, colorRED)
    screen.blit(over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 10))
    pygame.display.flip()
    pygame.time.delay(2000)

FPS = 5
clock = pygame.time.Clock()

food = Food()
snake = Snake()
food.generate_random_pos(snake.body)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Arrow key controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)
    draw_grid()

    snake.move()
    snake.check_collision(food)

    # If food disappeared after timer, generate new one
    if food.is_expired():
        food.generate_random_pos(snake.body)

    # If snake hits itself
    if snake.check_self_collision():
        game_over()
        running = False

    snake.draw()
    food.draw()
    show_score(snake.score)
    show_food_info(food)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()