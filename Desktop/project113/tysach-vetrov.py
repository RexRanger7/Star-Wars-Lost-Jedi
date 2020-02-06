import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 710
HEIGHT = 750
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
start_screen_flag = True


def start_screen():
    global start_screen_flag
    intro_text = ["Звёздные Войны: Потерянный Джедай", "",
                  "Предыстория:",
                  "В данный момент вы джедай - Энакин Скайуокер.",
                  "Вы участвовали в штурме планеты Кристофсис в ходе Войн Клонов.",
                  "Победа за вами, но к сожалению вам пришлось идти в ",
                  "рискованное наступление одному.",
                  "Вы выполнили своё задание успешно, но к сожалению теперь",
                  "вам приходится возвращаться в храм джедаев ",
                  "на маленьком истребителе.",
                  "Беда настигла вас быстро, ведь недалеко от Кристофсиса ",
                  "вы попали в пояс астероидов.",
                  "Теперь дорога домой лежит только через него.",
                  "Удачи!",
                  "Правила игры:",
                  "A - перемещение влево.",
                  "D - перемещени вправо.",
                  "J - Стрелять.",
                  "Чтобы перейти в игру кликнете мышкой."]

    fon = pygame.transform.scale(pygame.image.load('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start_screen_flag = False
                return

        pygame.display.flip()
        clock.tick(FPS)



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars: Lost Jedi")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def enemy1():
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)


def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, WHITE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Jedi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = random.choice(meteor_images)
        self.image1.set_colorkey(BLACK)
        self.image = self.image1.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 9)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + \
                10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


background = pygame.image.load(path.join(img_dir, "fon.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip2_red.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue12.png")).convert()
meteor_images = []
meteor_list = ['meteorGrey_big1.png', 'meteorGrey_big4.png',
               'meteorGrey_med2.png', 'meteorGrey_small1.png',
               'meteorGrey_small2.png', 'meteorGrey_tiny1.png',
               'meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Jedi()
all_sprites.add(player)
for i in range(14):
    enemy1()
score = 0


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 100 - int(hit.radius)
        enemy1()

    hits = pygame.sprite.spritecollide\
        (player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius * 2
        enemy1()
        if player.health <= 0:
            running = False
    screen.fill(WHITE)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health_bar(screen, 5, 5, player.health)
    if start_screen_flag is True:
        start_screen()
    pygame.display.flip()


pygame.quit()