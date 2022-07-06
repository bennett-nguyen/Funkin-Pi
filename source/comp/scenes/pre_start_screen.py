import pygame
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
        if self.display_message[0]:
            ds.screen.blit(self.message_list[0][0], self.message_list[0][1])
        if self.display_message[1]:
            ds.screen.blit(self.message_list[1][0], self.message_list[1][1])
        if self.display_message[2]:
            ds.screen.blit(self.message_list[2][0], self.message_list[2][1])


    def redraw(self):
        self.current_time = pygame.time.get_ticks()

        if self.current_time - self.displayed_time >= self.delay_display:
            if not self.display_message[0]:
                self.displayed_time = pygame.time.get_ticks()
                self.display_message[0] = True
            elif not self.display_message[1]:
                self.displayed_time = pygame.time.get_ticks()
                self.display_message[1] = True
            elif not self.display_message[2]:
                self.displayed_time = pygame.time.get_ticks()
                self.display_message[2] = True
                self.redirect = self.redirect_code
        
        self.draw_message()