import pygame
from game_components import FlyingSurf
from game_loader import Image, DisplaySurf

player_surface_x = (DisplaySurf.WIDTH/2/2)*3
enemy_surface_x = DisplaySurf.WIDTH/2/2

# Wrote for testing
flying_object_enemy = FlyingSurf(enemy_surface_x, 875, Image.ACTIVATED_LEFT_ARROW) 

flying_object = FlyingSurf(player_surface_x, 875, Image.ACTIVATED_LEFT_ARROW, True)
flying_object_sick = FlyingSurf(player_surface_x, 920, Image.ACTIVATED_LEFT_ARROW, True)
flying_object_3 = FlyingSurf(player_surface_x, 1000, Image.ACTIVATED_DOWN_ARROW, True)
flying_object_2 = FlyingSurf(player_surface_x, 1125, Image.ACTIVATED_UP_ARROW, True)
flying_object_4 = FlyingSurf(player_surface_x, 1250, Image.ACTIVATED_RIGHT_ARROW, True)

objects = [flying_object_enemy, flying_object, flying_object_sick, flying_object_3, flying_object_2, flying_object_4]
# ------

pygame.init()