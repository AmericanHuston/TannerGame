from __future__ import annotations
import pygame
import math

#Sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color: pygame.Color, radius: float, speed: float, health: int, damage_spacing: int, id: str = "Sprite"):
        super().__init__()
        self.id = id
        self.damage_spacing = damage_spacing
        self.radius = radius
        self.color = color
        self.last_time_damage_taken = damage_spacing + 1
        self.health = health
        self.speed = speed
        self.image = pygame.Surface((radius*2, radius*2))
        self.image.set_colorkey("green")
        self.image.fill("green")

        pygame.draw.circle(self.image, self.color,((radius), (radius)), radius)
        
        self.rect = self.image.get_rect()
        print("Created Sprite")
    def decrease_health(self, reason: str, amount: float):
        if pygame.time.get_ticks() > self.last_time_damage_taken + self.damage_spacing:
            self.health -= amount
            self.last_time_damage_taken = pygame.time.get_ticks()
            print(reason, " ", amount)
    def increase_health(self, reason: str, amount: float):
        self.health += amount
        print(reason, " ", amount)
    def check_health(self):
        if self.health <= 0:
            return False
        else:
            return True

    def move_towards_player(self, other: Sprite):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = other.rect.x - self.rect.x, other.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist <= 10:
            other.decrease_health("enemy", 1)
            dx, dy = dx / dist, dy / dist 
        else:
            dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    # Same thing using only pygame utilities
    def move_towards_player2(self, player: Sprite):
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