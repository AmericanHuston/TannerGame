import pygame
import random
import math
from pygame.locals import *
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
running = True
dt = 0
# mixer.init()
# mixer.music.load("BreathDemo.wav")
# mixer.music.set_volume(1.0)
# mixer.music.play()

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500

player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
enemy_pos = pygame.Vector2(random.randrange(0, 1080), random.randrange(0,720))

#Sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, radius, speed, health):
        super().__init__()
        self.color = color
        self.last_time_damage_taken = 501
        self.health = health
        self.speed = speed
        self.image = pygame.Surface((radius*2, radius*2))
        self.image.set_colorkey("green")
        self.image.fill("green")

        pygame.draw.circle(self.image, self.color,((radius), (radius)), radius)
        
        self.rect = self.image.get_rect()
        print(color)
    def decrease_health(self, reason, amount):
        if pygame.time.get_ticks() > self.last_time_damage_taken + 200:
            self.health -= amount
            self.last_time_damage_taken = pygame.time.get_ticks()
            print(reason, " ", amount)
    def increase_health(self, reason, amount):
        self.health += amount
        print(reason, " ", amount)
    def check_health(self):
        if self.health <= 0:
            return False
        else:
            return True

    def move_towards_player(self, other):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = other.rect.x - self.rect.x, other.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist <= 10:
            other.decrease_health("enemy", 1)
        else:
            dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    # Same thing using only pygame utilities
    def move_towards_player2(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)

    def moveRight(self):
        self.rect.x += self.speed

    def moveLeft(self):
        self.rect.x -= self.speed

    def moveForward(self):
        self.rect.y += self.speed * self.speed/10

    def moveBack(self):
        self.rect.y -= self.speed * self.speed/10

class HealthBar():
    def __init__(self, x, y, w, h, max_hp, colorBottom, colorTop):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio = self.hp / self.max_hp
        self.colorBottom = colorBottom
        self.colorTop = colorTop

    def set_hp(self, hp):
        self.hp = hp

    def draw(self, surface):
        self.ratio = self.hp / self.max_hp
        #Health bar
        pygame.draw.rect(surface, self.colorBottom, (self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface, self.colorTop, (self.x, self.y, self.w * self.ratio, self.h))

all_sprites_list = pygame.sprite.Group()

brown = (255, 153, 0)
silver = (192, 192, 192)
Player = Sprite(brown, 30, 10, 10)
Player.rect.x = player_pos.x
Player.rect.y = player_pos.y

Enemy = Sprite(silver, 40, 8, 2)
Enemy.rect.x = enemy_pos.x
Enemy.rect.y = enemy_pos.y

all_sprites_list.add(Player)
all_sprites_list.add(Enemy)

p_health_bar = HealthBar(40, 40, 1000, 30, 10, "red", "green")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
    screen.fill("black")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        Player.moveBack()
    if keys[pygame.K_s]:
        Player.moveForward()
    if keys[pygame.K_a]:
        Player.moveLeft()
    if keys[pygame.K_d]:
        Player.moveRight()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_q]:
        running = False

    #enemy logic
    Enemy.move_towards_player(Player)

    p_health_bar.set_hp(Player.health)
    p_health_bar.draw(screen)

    #makes next screen get rendered
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    if running:
        running = Player.check_health()
    pygame.display.flip()

    #framerate
    dt = clock.tick(30) / 1000

pygame.quit()

#