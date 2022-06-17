import pygame
import time
from load.game_loader import DisplaySurf, Audio
from scene.component import SceneSwitcher
from scene.scenes import StartScreen, MenuScreen, MainGame
from sys import exit

pygame.init()

# Audio.FREAKY_MENU.play(-1)

game_scenes = {
    "start screen": StartScreen(),
    "menu screen": MenuScreen(),
    "main game": MainGame()
}

switcher = SceneSwitcher(game_scenes)


def game():
    dt = 0 # delta time
    prev_time = time.time()

    while True:
        DisplaySurf.Screen.fill('Black')
        DisplaySurf.Clock.tick(DisplaySurf.FPS)
        
        now = time.time()
        dt = now - prev_time
        prev_time = now
        
        events = pygame.event.get()
        switcher.receive_events(events)
        switcher.receive_dt(dt)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        switcher.update()
        pygame.display.update()
        
if __name__ == "__main__":
    game()