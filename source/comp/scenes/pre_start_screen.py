import pygame as pg
import source.load.ds as ds
from source.load.template import Scene


class PreStartScreen(Scene):
    def __init__(self, message_list, delay_display, delay_transition, redirect_code):
        super().__init__()
        self.message_list = message_list
        self.display_message = [False, False, False]
        self.redirect_code = redirect_code

        self.delay_display = delay_display
        self.redirect_delay = delay_transition
        self.deactivate_fade = True
        self.current_time = 0
        self.displayed_time = 0

    def draw_message(self):
        for index, flag in enumerate(self.display_message):
            if flag:
                ds.screen.blit(self.message_list[index][0], self.message_list[index][1])

    def redraw(self):
        self.current_time = pg.time.get_ticks()

        if self.current_time - self.displayed_time >= self.delay_display:
            for index, flag in enumerate(self.display_message):
                if not flag:
                    self.displayed_time = pg.time.get_ticks()
                    self.display_message[index] = True
                    if self.display_message[2]:
                        self.redirect = self.redirect_code
                    break

        self.draw_message()