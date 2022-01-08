import pygame
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
        i.move()
        i.draw_arrow()
        i.move_arrow()

        if i.rect.y <= - i.surface.get_height():
            i.rect.y = DisplaySurf.HEIGHT + i.surface.get_height()
            i.arrow_rect.y = i.rect.y - 20

    pygame.display.update()



while True:
    key = pygame.key.get_pressed()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            for i in objects[:]:
                if i.rect.colliderect(transparent_rect.rect): # and event.key == key[K_SPACE]:
                    print("deleted")
                    objects.remove(i)



    draw_window()
    DisplaySurf.Clock.tick(DisplaySurf.FPS)
