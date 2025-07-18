import pygame
import Sprite as Sp
import variables
import math

Sprite = Sp.Sprite

def calc_dist(item1, item2):
    dx, dy = item2.rect.x - item1.rect.x, item2.rect.y - item1.rect.y
    return math.hypot(dx, dy)

class Item(): #TODO add images for items
    def __init__(self, durration: float, type: str):
        self.id = id
        self.durration = durration
        self.type = type
        self.x = 0
        self.y = 0
        self.rect = pygame.Vector2(self.x, self.y)
        self.used = 0
        self.attached = False
        print("Created Item")
    def set_cordinates(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
    def set_type(self, type: str):
        self.type = type
    def attach(self, attach_to_object: Sprite):
            if self.type == variables.possible_items[0]:
                print("stuff 0 happened")
                self.rect.x = attach_to_object.rect.x + attach_to_object.radius
                self.rect.y = attach_to_object.rect.y
            elif self.type == variables.possible_items[1]:
                print("stuff 1 happened")
                self.rect.x = attach_to_object.rect.x + attach_to_object.radius
                self.rect.y = attach_to_object.rect.y
            elif self.type == variables.possible_items[2]:
                print("stuff 2 happened")
                self.rect.x = attach_to_object.rect.x + attach_to_object.radius
                self.rect.y = attach_to_object.rect.y
            else:
                print("this should never happen...")
            self.attached = True
    def detach(self):
        print("Detached Item")
        self.attached = False
    def draw(self, surface: pygame.surface.Surface):
        #need to use self.rect.x and self.rect.y on all of these
        if self.type == "ranged_weapon": #TODO add functionality
            ranged_weapon = pygame.draw.rect(surface, "silver", (self.rect.x, self.rect.y, 4, 9))
            ranged_weapon.x = self.rect.x
            ranged_weapon.y = self.rect.y
        if self.type == "close_weapon": #TODO add functionality
            close_weapon = pygame.draw.rect(surface, "silver", (self.rect.x, self.rect.y, 4, 15))
            close_weapon.x = self.rect.x
            close_weapon.y = self.rect.y
        if self.type == "healer":
            pygame.draw.circle(surface, "red", (self.rect.x, self.rect.y), 6)
    def is_attached(self):
        return self.attached
    def can_use(self):
        return not self.used
    def use(self, user: Sprite, target: Sprite): #TODO check item durration for weapons (dissable use before time is up)
        if self.type == "healer" and self.is_attached():
            user.increase_health("Used Healer", 1)
            self.detach()
            self.used = 1
        elif self.type == "ranged_weapon" and self.is_attached():
            print("need to fill this (ranged_weapon)")
            self.detach() #todo Remove after checking durration
            self.used = 1
        elif self.type == "close_weapon" and self.is_attached():
            print("need to fill this (close_weapon)")
            if calc_dist(self, target) < 40:
                target.decrease_health("Player used a weapon!", 1)
                self.detach()
                self.used = 1
            else:
                print("Enemy was too far away...")
    def unuse(self):
        self.used = 0
