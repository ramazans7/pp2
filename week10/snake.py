import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

# создаем окно игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# цвета
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

# шрифт для текста
font = pygame.font.SysFont("Verdana", 20)

# рисуем сетку
def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (j * CELL, i * CELL, CELL, CELL), 1)

# точка (координаты)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# змейка
class Snake:
    def __init__(self):
        # тело змейки (список точек)
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        # направление движения
        self.dx = 0
        self.dy = -1
        # счет
        self.score = 0

    def move(self):
        # двигаем тело
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # двигаем голову
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # телепорт через границы
        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1

    def draw(self):
        # рисуем голову
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        # рисуем тело
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        # если съели еду
        if head.x == food.pos.x and head.y == food.pos.y:
            # увеличиваем змейку
            self.body.append(Point(self.body[-1].x, self.body[-1].y))
            self.score += 1
            # генерируем новую еду
            food.generate_random_pos(self.body)

    def check_self_collision(self):
        head = self.body[0]
        # проверка столкновения с собой
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

# еда
class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        # ищем свободное место
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

# вывод счета
def show_score(score):
    text = font.render(f"Score: {score}", True, colorWHITE)
    screen.blit(text, (10, 10))

# экран проигрыша
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

        # управление стрелками
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

    # если врезались в себя
    if snake.check_self_collision():
        game_over()
        running = False

    snake.draw()
    food.draw()
    show_score(snake.score)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()