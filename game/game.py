import pygame
from load.game_loader import DisplaySurf, Audio, Gallery
from game.component import Entity, TransparentSurf
from sys import exit
from mapping import file_loader, processor

# !-- THIS FILE IS FOR REFERENCING ONLY --! #

pygame.init()

objects = processor(file_loader())

current_time = 0

while True:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    player_surface.up_arrow = Gallery.ACTIVATED_UP_ARROW
                    player_entity.draw_self()

                case pygame.K_DOWN:
                    player_surface.down_arrow = Gallery.ACTIVATED_DOWN_ARROW
                    player_entity.draw_self()

                case pygame.K_LEFT:
                    player_surface.left_arrow = Gallery.ACTIVATED_LEFT_ARROW
                    player_entity.draw_self()

                case pygame.K_RIGHT:
                    player_surface.right_arrow = Gallery.ACTIVATED_RIGHT_ARROW
                    player_entity.draw_self()

            for object in objects[:]:
                if object.key == event.key:
                    if object.collide(player_surface):
                        objects.remove(object)
                        break

        if event.type == pygame.KEYUP:
            player_surface.event_on_arrow_deactivate(event)
            
    draw_window(current_time)
    DisplaySurf.Clock.tick(DisplaySurf.FPS)
