import pygame
import time
import general_component.constant as const
from load.game_loader import DisplaySurf, Audio, Message, shared_data
from scene.component import SceneSwitcher
from scene.scenes import StartScreen, MenuScreen, MainGame, PreStartScreen
from sys import exit

pygame.init()

game_scenes = {
    "pre start screen 1": PreStartScreen(Message._req_message_list_1, 700, 800, "pre start screen 2"),
    "pre start screen 2": PreStartScreen(Message._req_message_list_2, 700, 800, "pre start screen 3"),
    "pre start screen 3": PreStartScreen(Message._req_message_list_3, 700, 800, "pre start screen 4"),
    "pre start screen 4": PreStartScreen(Message._opt_message_list, 700, 1000, "start screen"),
    "start screen": StartScreen(),
    "menu screen": MenuScreen(),
    "main game": MainGame()
}

switcher = SceneSwitcher(game_scenes, start="pre start screen 1")

def game():
    Audio.FREAKY_MENU.play(-1)
    dt = 0 # delta time
    prev_time = time.time()

    while True:
        DisplaySurf.Screen.fill('Black')
        DisplaySurf.Clock.tick(const.FPS)
        
        now = time.time()
        dt = float(now - prev_time)
        prev_time = now
        
        events = pygame.event.get()
        shared_data.dt = dt
        shared_data.events = events
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        switcher.update()
        pygame.display.update()
        
if __name__ == "__main__":
    game()