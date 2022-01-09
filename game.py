import pygame
from pygame.constants import K_UP
from game_loader import DisplaySurf
from ui_componets import transparent_rect, transparent_rect2, objects 
from sys import exit

drawn = []

pygame.init()


def draw_window():
    DisplaySurf.Screen.fill('Black')

    DisplaySurf.Screen.blit(transparent_rect.surface, transparent_rect.rect)
    DisplaySurf.Screen.blit(transparent_rect.surface, transparent_rect2.rect)
    transparent_rect.draw_arrow()
    transparent_rect2.draw_arrow()
 
    pygame.draw.line(DisplaySurf.Screen, "White", (DisplaySurf.WIDTH/2,
                     0), (DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT), 3)

    for i in objects:
        DisplaySurf.Screen.blit(i.surface, i.rect)
        i.draw_arrow()
        
        i.move()
        i.move_arrow()

        if i.rect.y <= - i.surface.get_height():
            i.rect.y = DisplaySurf.HEIGHT + i.surface.get_height()
            i.arrow_rect.y = i.rect.y

    pygame.display.update()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
 
        if event.type == pygame.KEYDOWN:
            for object in objects[:]:
                if object.rect.colliderect(transparent_rect.rect):
                    match event.key:
                        case pygame.K_UP:
                            objects.remove(object) if object.key == "up" else None

                        case pygame.K_DOWN:
                            objects.remove(object) if object.key == "down" else None

                        case pygame.K_LEFT:
                            objects.remove(object) if object.key == 'left' else None

                        case pygame.K_RIGHT:
                            objects.remove(object) if object.key == 'right' else None

    draw_window()
    DisplaySurf.Clock.tick(DisplaySurf.FPS)
