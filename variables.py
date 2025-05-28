import pygame
import random

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
running = True
dt = 0
possible_items = ["healer", "close_weapon", "ranged_weapon"]

player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
enemy_pos = pygame.Vector2(random.randrange(0, 1080), random.randrange(0,720))