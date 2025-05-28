import pygame
import Sprite

class Healthbar():
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
