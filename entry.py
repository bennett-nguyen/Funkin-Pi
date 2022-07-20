import time
import pygame as pg
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const

from sys import exit
from source.load.shared import shared_data
from source.load.switcher import SceneSwitcher
from source.comp.scenes.main_game import MainGame
from source.comp.scenes.menu_screen import MenuScreen
from source.comp.scenes.start_screen import StartScreen
from source.comp.scenes.pre_start_screen import PreStartScreen

pg.init()

game_scenes = {
    "pre start screen 1": PreStartScreen(assets.Message.req_message_list_1, 700, 800, "pre start screen 2"),
    "pre start screen 2": PreStartScreen(assets.Message.req_message_list_2, 700, 800, "pre start screen 3"),
    "pre start screen 3": PreStartScreen(assets.Message.req_message_list_3, 700, 800, "pre start screen 4"),
    "pre start screen 4": PreStartScreen(assets.Message.opt_message_list, 700, 1000, "start screen"),
    "start screen": StartScreen(),
    "menu screen": MenuScreen(),
    "main game": MainGame()
}

switcher = SceneSwitcher(game_scenes, start="pre start screen 1")

def game():
    pg.mixer.music.play(-1)
    dt = 0 # delta time
    prev_time = time.time()

    while True:
        ds.screen.fill('Black')
        ds.clock.tick(const.FPS)

        now = time.time()
        dt = float(now - prev_time)
        prev_time = now

        events = pg.event.get()
        shared_data.dt = dt
        shared_data.events = events

        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        switcher.update()
        pg.display.update()

if __name__ == "__main__":
    game()