import pygame
from load.game_loader import DisplaySurf, Audio, Gallery
from game_components import Entity, TransparentSurf
from sys import exit
from mapping import file_loader, processor

pygame.init()

objects = processor(file_loader())

player_surface_x = (DisplaySurf.WIDTH/2/2)*3
enemy_surface_x = DisplaySurf.WIDTH/2/2

player_entity = Entity(player_surface_x, DisplaySurf.HEIGHT/2)
enemy_entity = Entity(enemy_surface_x, DisplaySurf.HEIGHT/2)

enemy_surface = TransparentSurf(enemy_surface_x, 80)
player_surface = TransparentSurf(player_surface_x, 80)

current_time = 0

Audio.TUTORIAL.play()


def draw_window(current_time):
    DisplaySurf.Screen.fill('Black')

    if not player_entity.animation_is_playable():
        player_entity.change_animation(Gallery.ENTITY_IDLE)

    player_entity.load_animation()
    player_entity.draw_self()

    player_surface.draw_self()
    enemy_surface.draw_self()

    pygame.draw.line(DisplaySurf.Screen, "White", (DisplaySurf.WIDTH/2,
                     0), (DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT), 3)
    
    if current_time > file_loader()["initial value"]["time"] * 1000:
        for object in objects:
            object.draw_self()
            object.move()

            if object.rect.y <= - object.surface.get_height():
                objects.remove(object)

            if object.collide_for_enemy(enemy_surface):
                objects.remove(object)

                break

    pygame.display.update()

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
                    player_entity.change_animation(Gallery.ENTITY_UP)
                    player_entity.draw_self()

                case pygame.K_DOWN:
                    player_surface.down_arrow = Gallery.ACTIVATED_DOWN_ARROW
                    player_entity.change_animation(Gallery.ENTITY_DOWN)
                    player_entity.draw_self()

                case pygame.K_LEFT:
                    player_surface.left_arrow = Gallery.ACTIVATED_LEFT_ARROW
                    player_entity.change_animation(Gallery.ENTITY_LEFT)
                    player_entity.draw_self()

                case pygame.K_RIGHT:
                    player_surface.right_arrow = Gallery.ACTIVATED_RIGHT_ARROW
                    player_entity.change_animation(Gallery.ENTITY_RIGHT)
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