from __future__ import annotations
import pygame
import random
import math
from pygame.locals import *
from pygame import mixer
import argparse
import datetime
import Sprite as Sp
import Item as It
import HealthBar as Hb
import ItemBox as Ib

#-------Current version is 0.1.1-------#

parser = argparse.ArgumentParser(description="Checking version")
parser.add_argument("--version", action="store_true")
args = parser.parse_args()
if (args.version):
    with open("version.txt","w") as f:
        f.write("0.1.1") #current version goes here
    exit()

ItemBox = Ib.ItemBox
HealthBar = Hb.Healthbar
Item = It.Item
Sprite = Sp.Sprite
pygame.init()
try:
    mixer.init()
    mixer.music.load("BreathDemo.wav")
    mixer.music.set_volume(1.0)
    mixer.music.play()
except pygame.error:
    print("Can't run with audio today...Device not found")

screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
running = True
dt = 0
possible_items = ["healer", "close_weapon", "ranged_weapon"]
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500 
HEIGHT = 500
brown = (255, 153, 0)
silver = (192, 192, 192)
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
enemy_pos = pygame.Vector2(random.randrange(0, 1080), random.randrange(0,720))

def calc_dist(item1, item2):
    dx, dy = item2.rect.x - item1.rect.x, item2.rect.y - item1.rect.y
    return math.hypot(dx, dy)

all_sprites_list = pygame.sprite.Group()

box = ItemBox(
4,
(possible_items[random.randrange(0,2)]),
"box",
random.randrange(0, 1080),
random.randrange(0, 720)
)

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
p_health_bar = HealthBar(40, 40, 70, 10, Player.health, "red", "green", Player, screen)
e_health_bar = HealthBar(40, 40, 70, 10, Enemy.health, "red", "yellow", Enemy, screen)

all_sprites_list.add(Player)
all_sprites_list.add(Enemy)

while running:
    random.seed = datetime.time
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
        try:
            if dropped_item.can_use():
                dropped_item.use(Player, Enemy)
                if not dropped_item.is_attached():
                    box.revive()
                    box.set_cords(random.randrange(0, 1080), random.randrange(0, 720))
                    dropped_item.unuse()
                    dropped_item.set_type((possible_items[random.randrange(0,2)]))
        except NameError:
            print("Nu uh can't use what you don't have")
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_q]:
        running = False

    #enemy logic
    Enemy.move_towards_player(Player) #TODO attach Enemy health bar to enemy
    e_health_bar.attach(screen, Enemy)
    p_health_bar.update()
    e_health_bar.update()
    
    if not box.is_dead():
        box.draw(screen)
        box_health_bar.update()
        box.damage_box(Player)
    if box.is_dead():
        try:
            dropped_item
        except NameError:
            dropped_item = Item(box.durration, box.item_inside)
        if not dropped_item.is_attached() and dropped_item.can_use():
            dropped_item.set_cordinates(box.rect.x, box.rect.y)
            dropped_item.draw(screen)
        else:
            dropped_item.draw(screen)
        if dropped_item.can_use() and calc_dist(dropped_item, box.attacker) < 50: #todo Make this all independant of the box being alive or dead
            dropped_item.attach(box.attacker) #This makes a loop with the left shift key, need to find another way to see (fixed it now, keeping for historic value)

    #makes next screen get rendered
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    if not Enemy.check_health():
        all_sprites_list.remove(Enemy)
        Enemy.kill()

    if running:
        running = Player.check_health()
    pygame.display.flip()

    #framerate
    dt = clock.tick(30) / 1000

pygame.quit()