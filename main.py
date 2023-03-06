import pygame
import random
from pygame import mixer
pygame.font.init()
mixer.init()

my_font = pygame.font.SysFont(None, 30)
shoot = pygame.mixer.Sound('Sound/ShootSound.mp3')
enemy_shoot = pygame.mixer.Sound('Sound/laser1.wav')


clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

score = 0
score_increment = 10

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()

red = (255, 0, 0)
green = (0, 255, 0)

background = pygame.image.load('Graphics/Background.png')

# rolling background
w, h = background.get_size()
y = 0
y1 = - h

def rollingBackground():
    global y, y1, h
    screen.blit(background, (0, y))
    screen.blit(background, (0, y1))
    y += 1
    y1 += 1

    if y > h:
        y = -h
    if y1 > h:
        y1 = -h


def draw_background():
    screen.blit(background, (0, 0))


def score_increase():
    global score
    global score_increment

    score += score_increment
    print(score)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Ship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8
        cooldown = 300  # milliseconds

        # movement inputs
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        # shooting inputs
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
            shoot.play()

        if self.health_remaining <= 0:
            self.kill()
            quit()

        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            score_increase()
            self.kill()


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Invader' + str(random.randint(1, 6)) + '.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter -= 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.bottom > screen_height:
            self.kill()

        if pygame.sprite.spritecollide(self, spaceship_group, False):
            self.kill()
            spaceship.health_remaining -= 1


spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()


def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()


spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:

    rollingBackground()
    clock.tick(fps)
    text_surface = my_font.render('Score: ' + str(score), False, (255, 255, 255))

    time_now = pygame.time.get_ticks()
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0 :
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now
        enemy_shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    spaceship_group.update()
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    screen.blit(text_surface, (10, 10))



    pygame.display.flip()
    pygame.display.update()

pygame.quit()