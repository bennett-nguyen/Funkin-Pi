import pygame
from load.game_loader import DisplaySurf, Audio
from scene.component import SceneSwitcher
from scene.scenes import StartScreen, MenuScreen
from sys import exit

pygame.init()

# Audio.FREAKY_MENU.play(-1)

game_scenes = {
    "start screen": StartScreen(),
    "menu screen": MenuScreen(),
    "main game": None
}

switcher = SceneSwitcher(game_scenes)

def game():
    while True:
        DisplaySurf.Screen.fill('Black')
        DisplaySurf.Clock.tick(DisplaySurf.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        switcher.update()
        pygame.display.update()
        
if __name__ == "__main__":
    game()