import pygame
import math
import random
import Sprite as Sp
import variables
import datetime

Sprite = Sp.Sprite

random.seed = datetime.time

class ItemBox():
    def __init__(self, health: int, item_inside: str = (variables.possible_items[random.randrange(0,2)]), id: str = "box", x: int = 0, y: int = 0, box_size: int = 10, damage_spacing: int = 300):
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
    def revive(self, health = 4):
        self.item_inside = variables.possible_items[random.randrange(0,2)]
        self.health = health
    def set_cords(self, x, y):
        self.x = x
        self.y = y

