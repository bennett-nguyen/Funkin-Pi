import pygame
from game_loader import DisplaySurf, Audio, Image
from game_components import Entity, TransparentSurf
from sys import exit
from test import objects

pygame.init()


player_surface_x = (DisplaySurf.WIDTH/2/2)*3
enemy_surface_x = DisplaySurf.WIDTH/2/2

player_entity = Entity(player_surface_x, DisplaySurf.HEIGHT/2)
enemy_entity = Entity(enemy_surface_x, DisplaySurf.HEIGHT/2)

enemy_surface = TransparentSurf(enemy_surface_x, 80)
player_surface = TransparentSurf(player_surface_x, 80)


step_counter = 0
missed_counter = 0

current_time = 0
button_pressed_time = 0

# accuracy = missed_counter / (step_counter + missed_counter) * 100

# Audio.INSTRUMENT.play()
# Audio.VOCAL.play()

def draw_window():
    DisplaySurf.Screen.fill('Black')

    player_entity.draw_self()
    enemy_entity.draw_self()

    player_surface.draw_self()
    enemy_surface.draw_self()

    pygame.draw.line(DisplaySurf.Screen, "White", (DisplaySurf.WIDTH/2, 0), (DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT), 3)

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
                    player_surface.up_arrow = Image.ACTIVATED_UP_ARROW
                    player_entity.state = Image.ENTITY_UP
                    button_pressed_time = pygame.time.get_ticks()

                case pygame.K_DOWN:
                    player_surface.down_arrow = Image.ACTIVATED_DOWN_ARROW
                    player_entity.state = Image.ENTITY_DOWN
                    button_pressed_time = pygame.time.get_ticks()

                case pygame.K_LEFT:
                    player_surface.left_arrow = Image.ACTIVATED_LEFT_ARROW
                    player_entity.state = Image.ENTITY_LEFT
                    button_pressed_time = pygame.time.get_ticks()

                case pygame.K_RIGHT:
                    player_surface.right_arrow = Image.ACTIVATED_RIGHT_ARROW
                    player_entity.state = Image.ENTITY_RIGHT
                    button_pressed_time = pygame.time.get_ticks()
                
            for object in objects:
                if object.key == event.key:
                    if object.collide(player_surface):
                        objects.remove(object)
                        break

        if event.type == pygame.KEYUP:
            player_surface.event_on_arrow_deactivate(event)

    if current_time - button_pressed_time > 1500:
        player_entity.state = Image.ENTITY_IDLE

    draw_window()
    DisplaySurf.Clock.tick(DisplaySurf.FPS)