import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# НАСТРОЙКИ ЭКРАНА
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")


# ЦВЕТА
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
GREEN = (0, 180, 0)


# ШРИФТЫ
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 40)


# FPS И ЧАСЫ
clock = pygame.time.Clock()
FPS = 60

# ПАРАМЕТРЫ ДОРОГИ
ROAD_X = 50
ROAD_WIDTH = 300
LINE_WIDTH = 6
line_y = 0
road_speed = 6

# КЛАСС ИГРОКА
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Создаем простую машинку как прямоугольник
        self.image = pygame.Surface((50, 90), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLUE, (0, 0, 50, 90), border_radius=10)
        pygame.draw.rect(self.image, BLACK, (8, 10, 34, 20), border_radius=5)   # стекло
        pygame.draw.rect(self.image, BLACK, (8, 60, 34, 20), border_radius=5)   # задняя часть

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20

        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()

        # Движение влево
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Движение вправо
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Ограничиваем движение в пределах дороги
        if self.rect.left < ROAD_X:
            self.rect.left = ROAD_X

        if self.rect.right > ROAD_X + ROAD_WIDTH:
            self.rect.right = ROAD_X + ROAD_WIDTH


# КЛАСС ВРАЖЕСКОЙ МАШИНЫ
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 90), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, 50, 90), border_radius=10)
        pygame.draw.rect(self.image, BLACK, (8, 10, 34, 20), border_radius=5)
        pygame.draw.rect(self.image, BLACK, (8, 60, 34, 20), border_radius=5)

        self.rect = self.image.get_rect()
        self.reset_position()

        self.speed = random.randint(5, 9)

    def reset_position(self):
        # Случайная позиция на дороге
        self.rect.x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300, -100)

    def update(self):
        self.rect.y += self.speed

        # Если машина ушла вниз экрана, создаем заново сверху
        if self.rect.top > HEIGHT:
            self.reset_position()
            self.speed = random.randint(5, 9)


# КЛАСС МОНЕТЫ
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Создаем круглую монету
        size = 26
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, BLACK, (size // 2, size // 2), size // 2, 2)

        self.rect = self.image.get_rect()
        self.speed = 6
        self.reset_position()

    def reset_position(self):
        # Монета появляется случайно на дороге
        self.rect.x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - self.rect.width)
        self.rect.y = random.randint(-500, -100)

    def update(self):
        self.rect.y += self.speed

        # Если монета ушла вниз, создаем заново сверху
        if self.rect.top > HEIGHT:
            self.reset_position()


# ФУНКЦИЯ ОТРИСОВКИ ДОРОГИ
def draw_road():
    global line_y

    # Фон
    screen.fill(GREEN)

    # Дорога
    pygame.draw.rect(screen, DARK_GRAY, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

    # Боковые линии дороги
    pygame.draw.line(screen, WHITE, (ROAD_X, 0), (ROAD_X, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, HEIGHT), 4)

    # Разделительные линии
    line_y += road_speed
    if line_y >= 40:
        line_y = 0

    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - LINE_WIDTH // 2, y + line_y, LINE_WIDTH, 25))



# ФУНКЦИЯ ВЫВОДА ТЕКСТА
def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


# ФУНКЦИЯ GAME OVER
def game_over_screen(score, coins):
    screen.fill(BLACK)

    over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    coin_text = font.render(f"Coins: {coins}", True, YELLOW)
    restart_text = small_font.render("Press R to restart or Q to quit", True, WHITE)

    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, 180))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 260))
    screen.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, 310))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 380))

    pygame.display.flip()

    # Ждем действия пользователя
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# ОСНОВНАЯ ИГРА

def main():
    player = Player()

    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()

    all_sprites.add(player)

    # Создаем несколько врагов
    for _ in range(3):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Создаем монеты
    for _ in range(2):
        coin = Coin()
        all_sprites.add(coin)
        coins_group.add(coin)

    # Очки и монеты
    score = 0
    coin_count = 0

    # Таймер для увеличения счета
    score_timer = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()

        # Постепенно увеличиваем счет
        score_timer += 1
        if score_timer >= FPS // 2:
            score += 1
            score_timer = 0

        # Проверка столкновения с врагом
        if pygame.sprite.spritecollideany(player, enemies):
            restart = game_over_screen(score, coin_count)
            if restart:
                return

        # Проверка сбора монет
        collected_coins = pygame.sprite.spritecollide(player, coins_group, False)
        for coin in collected_coins:
            coin_count += 1
            coin.reset_position()

    
        draw_road()

        all_sprites.draw(screen)

        # Счет слева сверху
        draw_text(f"Score: {score}", small_font, WHITE, 10, 10)

        # Количество монет справа сверху
        coin_surface = small_font.render(f"Coins: {coin_count}", True, YELLOW)
        screen.blit(coin_surface, (WIDTH - coin_surface.get_width() - 10, 10))

        pygame.display.flip()



# ПЕРЕЗАПУСК ИГРЫ

while True:
    main()