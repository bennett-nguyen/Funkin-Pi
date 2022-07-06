import pygame
import source.load.ds as ds

pygame.init()

class SceneSwitcher:
    def __init__(self, scenes: dict, start: str):
        self.scenes = scenes
        self.current = self.scenes[start]
        self.is_transitioning = False
        self.redirect_delay = 0
        self.deactivate_fade = False

        self.current_time = 0
        self.redirected_time = 0
        
        self.screen = pygame.Surface(ds.screen.get_size())
        self.screen.fill((0, 0, 0))

        self.alpha = 0
        self.fade_delay = 0
        self.fade_state = "OUT"

    def change_scene(self):
        state = self.current.redirect
        main_game_data = getattr(self.current, 'loaded_data', None)
        self.current.reset_attr()
        self.current = self.scenes[state]
        if main_game_data is not None:
            self.current.receive_data(main_game_data)
        self.reset_attr()

    def fade(self):
        if self.fade_state == "OUT":
            self.alpha += 4
            self.screen.set_alpha(self.alpha)
            ds.screen.blit(self.screen, (0, 0))

            if self.alpha >= 255:
                self.fade_state = "IN"

        elif self.fade_state == "IN":
            self.alpha -= 4
            self.screen.set_alpha(self.alpha)
            ds.screen.blit(self.screen, (0, 0))

            if self.alpha <= 0:
                self.fade_state = "OUT"
                self.alpha = 0
                self.fade_delay = 0
                self.is_transitioning = False

    def update(self):
        self.current_time = pygame.time.get_ticks()

        if not self.current.end_pre_event():
            self.current.pre_event()
        
        if not self.is_transitioning:
            self.current.input()
        self.current.redraw()

        if self.current.redirect is not None:
            if not self.redirected_time:
                self.redirected_time = pygame.time.get_ticks()
                self.redirect_delay = self.current.redirect_delay
                self.deactivate_fade = self.current.deactivate_fade
                
                if not self.deactivate_fade:
                    self.fade_delay = self.current.fade_delay
                    self.is_transitioning = True

            if self.current_time - self.redirected_time > self.redirect_delay:
                self.change_scene()

        if (
            self.is_transitioning and not self.deactivate_fade
            and self.current_time - self.redirected_time > self.fade_delay
        ):
            self.fade()

    def reset_attr(self):
        self.redirect_delay = self.redirected_time = 0
        self.deactivate_fade = False