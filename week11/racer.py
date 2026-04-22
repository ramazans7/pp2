import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (60, 60, 60)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 180, 0)
BRONZE = (205, 127, 50)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)

font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 40)

clock = pygame.time.Clock()
FPS = 60

ROAD_X = 50
ROAD_WIDTH = 300
line_y = 0
road_speed = 6

# каждые 5 очков монет — ускорение врагов
SPEED_UP_EVERY = 5


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < ROAD_X:
            self.rect.left = ROAD_X
        if self.rect.right > ROAD_X + ROAD_WIDTH:
            self.rect.right = ROAD_X + ROAD_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, level=0):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.level = level
        self.speed = random.randint(5, 9)
        self.reset()

    def reset(self):
        self.rect.x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - 50)
        self.rect.y = random.randint(-300, -100)

    def set_level(self, level):
        self.level = level
        self.speed = random.randint(5, 9) + level

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        # случайный вес
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            size = 20
            color = BRONZE
        elif self.weight == 2:
            size = 26
            color = SILVER
        else:
            size = 32
            color = GOLD

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - size)
        self.rect.y = random.randint(-500, -100)
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()


def draw_road():
    global line_y
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GRAY, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

    line_y += road_speed
    if line_y >= 40:
        line_y = 0

    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + line_y, 6, 25))


def game():
    player = Player()

    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    level = 0
    coin_count = 0

    for _ in range(3):
        e = Enemy(level)
        all_sprites.add(e)
        enemies.add(e)

    for _ in range(2):
        c = Coin()
        all_sprites.add(c)
        coins.add(c)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()

        # столкновение с врагом
        if pygame.sprite.spritecollideany(player, enemies):
            return

        # сбор монет
        for coin in pygame.sprite.spritecollide(player, coins, False):
            coin_count += coin.weight
            coin.reset()

            new_level = coin_count // SPEED_UP_EVERY
            if new_level > level:
                level = new_level
                for e in enemies:
                    e.set_level(level)

        draw_road()
        all_sprites.draw(screen)

        screen.blit(font.render(f"Coins: {coin_count}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 40))

        pygame.display.flip()


while True:
    game()