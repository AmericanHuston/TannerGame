from __future__ import annotations
import pygame
import random
import math
from pygame.locals import *
from pygame import mixer
import Sprite as Sp
import Item as It

#TODO Split objects into their own files
Item = It.Item
Sprite = Sp.Sprite
pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
running = True
dt = 0
possible_items = ["healer", "close_weapon", "ranged_weapon"]
mixer.init()
mixer.music.load("BreathDemo.wav")
mixer.music.set_volume(1.0)
mixer.music.play()

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500

player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
enemy_pos = pygame.Vector2(random.randrange(0, 1080), random.randrange(0,720))

class HealthBar():
    def __init__(self, x, y, w, h, max_hp, colorBottom, colorTop, attach_to, surface):
        self.surface = surface
        self.attached_to_object = attach_to
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio = self.hp / self.max_hp
        self.colorBottom = colorBottom
        self.colorTop = colorTop
        print("Created HealthBar")
    def set_hp(self, hp: int):
        self.hp = hp
    def draw(self, surface: pygame.surface.Surface, x: int = 0, y: int = 0):
        self.ratio = self.hp / self.max_hp
        #Health bar
        if x == 0 and y == 0:
            pygame.draw.rect(surface, self.colorBottom, (self.x,self.y,self.w,self.h))
            pygame.draw.rect(surface, self.colorTop, (self.x, self.y, self.w * self.ratio, self.h))
        else:
            pygame.draw.rect(surface, self.colorBottom, (x,y,self.w,self.h))
            pygame.draw.rect(surface, self.colorTop, (x, y, self.w * self.ratio, self.h))
    def attach(self, surface: pygame.surface.Surface, attach_to: Sprite):
        self.x = attach_to.rect.x
        self.y = attach_to.rect.y - attach_to.radius
    def update(self):
        self.draw(self.surface)
        self.attach(self.surface, self.attached_to_object)
        self.set_hp(self.attached_to_object.health)

class ItemBox():
    def __init__(self, health: int, item_inside: str = (possible_items[random.randrange(0,2)]), id: str = "box", x: int = 0, y: int = 0, box_size: int = 10, damage_spacing: int = 300):
        self.damage_spacing = damage_spacing
        self.last_time_damage_taken = damage_spacing + 1
        self.item_inside = item_inside
        self.box_size = box_size
        self.radius = box_size*2 #For compatability with healthbar
        if self.item_inside == "healer":
            self.durration = 10
        elif self.item_inside == "close_weapon":
            self.durration = 20
        elif self.item_inside == "ranged_weapon":
            self.durration = 15
        else:
            print("ItemBox ran into an error: Incorrect self.item_inside, invalid type")
        self.health = health
        self.id = id
        self.possible_items = ["healer", "close_weapon", "ranged_weapon"]
        print("Created ItemBox")
    def draw(self, surface: pygame.surface.Surface, x: int = random.randrange(0, 1080), y: int = random.randrange(0, 720)):
        self.rect = pygame.draw.rect(surface, "brown", (x, y, self.box_size, self.box_size))
        self.rect.x = x
        self.rect.y = y
    def damage_box(self, check_object: Sprite, damage_to_box: int = 1):
        dx, dy = check_object.rect.x - self.rect.x, check_object.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist <= 30 and pygame.time.get_ticks() > self.last_time_damage_taken + self.damage_spacing:
            self.attacker = check_object
            self.decrease_health(check_object, damage_to_box, check_object.id)
            self.last_time_damage_taken = pygame.time.get_ticks()
    def decrease_health(self, attacker: Sprite, amount: int = 1, reason: str = "default"):
        self.health -= amount
        print(self.id, reason, amount)
        if self.health <= 0:
            print("killed box, dropping:", self.item_inside)
            return attacker, self.item_inside, self.durration
    def get_possible_items(self):
        return self.possible_items
    def is_dead(self):
        if self.health == 0:
            return True
        else:
            return False
    def revive(self):
        self.item_inside

def calc_dist(item1, item2):
    dx, dy = item2.rect.x - item1.rect.x, item2.rect.y - item1.rect.y
    return math.hypot(dx, dy)


box = ItemBox(
4,
(possible_items[random.randrange(0,2)]),
"box",
random.randrange(0, 1080),
random.randrange(0, 720)
)

all_sprites_list = pygame.sprite.Group()

brown = (255, 153, 0)
silver = (192, 192, 192)
Player = Sprite(
brown,
30,
10,
10,
200,
"Player") #TODO add images
Player.rect.x = player_pos.x
Player.rect.y = player_pos.y

Enemy = Sprite(
silver,
40,
8,
2,
0,
"Enemy") #TODO add images
Enemy.rect.x = enemy_pos.x
Enemy.rect.y = enemy_pos.y

box_health_bar = HealthBar(40, 40, 50, 10, 4, "red", "green", box, screen)

all_sprites_list.add(Player)
all_sprites_list.add(Enemy)

p_health_bar = HealthBar(40, 40, 70, 10, 10, "red", "green", Player, screen)

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
    if keys[pygame.K_LSHIFT]:
        if dropped_item.can_use():
            dropped_item.use(Player)
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_q]:
        running = False

    #enemy logic
    Enemy.move_towards_player(Player) #TODO attach Enemy health bar to enemy

    p_health_bar.update()

    try:
        dropped_item
    except NameError:
        dropped_item = Item(box.durration, box.item_inside)
    
    if not box.is_dead():
        box.draw(screen)
        box_health_bar.update()
        box.damage_box(Player)
    if box.is_dead():
        if not dropped_item.is_attached() and dropped_item.can_use():
            dropped_item.set_cordinates(box.rect.x, box.rect.y)
            dropped_item.draw(screen)
        if dropped_item.can_use() and calc_dist(dropped_item, box.attacker) < 50: #todo add a delay to this (delay checking if the player is near the item)
            dropped_item.attach(box.attacker) #This makes a loop with the left shift key, need to find another way to see (fixed it now, keeping for historic value)
    if dropped_item.is_attached():
        dropped_item.draw(screen)

    #makes next screen get rendered
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    if running:
        running = Player.check_health()
    pygame.display.flip()

    #framerate
    dt = clock.tick(30) / 1000

pygame.quit()