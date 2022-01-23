import pygame
from game_loader import DisplaySurf, Audio
from game_components import StartScreen, MenuScreen
from sys import exit

pygame.init()

# Audio.FREAKY_MENU.play(-1)


scenes = {
    "start screen": StartScreen(),
    "menu screen": MenuScreen(),
    "main game": None
}


def game():
    while True:
        DisplaySurf.Screen.fill('Black')
        DisplaySurf.Clock.tick(DisplaySurf.FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        # scenes["menu screen"].update()
        # pygame.display.update()
        
if __name__ == "__main__":
    game()