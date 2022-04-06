import pygame
import load.game_loader as game_loader

pygame.init()

class Scene:
    def __init__(self):
        self.redirect = None
        self.redirect_delay = 0
        
        self.fade_delay = 0
    
    def input(self):
        pass
    
    def redraw(self):
        pass
    
    def reset_attr(self):
        self.redirect = None
    
    def set_direct(self):
        pass


class SceneSwitcher:
    def __init__(self, scenes: dict):
        self.scenes = scenes
        self.current = self.scenes["start screen"]
        self.is_transitioning = False
        self.redirect_delay = 0
        
        self.current_time = 0
        self.redirected_time = 0
        
        self.surface = pygame.Surface(game_loader.DisplaySurf.Screen.get_size())
        self.surface.fill((0, 0, 0))
        
        self.alpha = 0
        self.fade_delay = 0
        self.fade_state = "OUT"
        
    def change_scene(self):
        state = self.current.redirect
        self.current.reset_attr()
        self.current = self.scenes[state]
        self.reset_attr()
    
    def fade(self):
        if self.fade_state == "OUT":
            self.alpha += 4
            self.surface.set_alpha(self.alpha)
            game_loader.DisplaySurf.Screen.blit(self.surface, (0, 0))
            
            if self.alpha >= 255:
                self.fade_state = "IN"

        elif self.fade_state == "IN":
            self.alpha -= 4
            self.surface.set_alpha(self.alpha)
            game_loader.DisplaySurf.Screen.blit(self.surface, (0, 0))
            
            if self.alpha <= 0:
                self.fade_state = "OUT"
                self.alpha = 0
                self.is_transitioning = False
                self.fade_delay = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()

        if not self.is_transitioning:
            self.current.input()
        self.current.redraw()

        if self.current.redirect is not None:
            if not self.redirected_time:
                self.redirected_time = pygame.time.get_ticks()
                self.redirect_delay = self.current.redirect_delay
                self.fade_delay = self.current.fade_delay
                self.is_transitioning = True

            if self.current_time - self.redirected_time > self.redirect_delay:
                self.change_scene()

        if (
            self.is_transitioning
            and self.current_time - self.redirected_time > self.fade_delay
        ):
            self.fade()

    def reset_attr(self):
        self.redirect_delay = self.redirected_time = 0