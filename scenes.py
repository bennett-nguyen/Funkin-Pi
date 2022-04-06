import pygame
import game_loader
from game_components import ImageAnimation, Surface, description_parser, file_parser

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




class StartScreen(Scene):
    def __init__(self):
        super().__init__()
        self.sound_1_effect_played = self.sound_2_effect_played = self.button_pressed = False
        
        self.redirect = None
        self.redirect_delay = 3500
        
        self.fade_delay = 2500
        
        # custom fade in animation
        self.surf = pygame.Surface(game_loader.DisplaySurf.Screen.get_size())
        self.surf.fill((255, 255, 255))
        
        self.alpha = 255
        # ----

        self.deactivated_button = ImageAnimation(
            game_loader.Gallery.BUTTON_DEACTIVATED_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.1)
        self.on_hover_button = ImageAnimation(
            game_loader.Gallery.BUTTON_ON_HOVER_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.1)
        self.activated_button = ImageAnimation(
            game_loader.Gallery.BUTTON_ACTIVATED_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.15)
        self.button_hit_box = Surface(
            game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 250, 120)
        

    def redraw(self):
        game_loader.DisplaySurf.Screen.blit(game_loader.Gallery.LOGO, game_loader.Gallery.LOGO.get_rect(
            center=(game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2)))

        if self.button_pressed:
            self.activated_button.toggle_animation()
            self.redirect = "menu screen"

        if not self.button_pressed:
            if self.button_hit_box.rect.collidepoint(pygame.mouse.get_pos()):
                self.on_hover_button.toggle_animation()

                if not self.sound_2_effect_played:
                    game_loader.Audio.SCROLL_MENU.play()
                    self.sound_2_effect_played = True
            else:
                self.deactivated_button.toggle_animation()
                self.sound_2_effect_played = False
                
        if self.alpha > -1:
            self.custom_fade_in()

    def input(self):
        if (
            pygame.mouse.get_pressed()[0]
            and self.button_hit_box.rect.collidepoint(pygame.mouse.get_pos())
        ) or (pygame.key.get_pressed()[pygame.K_RETURN]):
            self.button_pressed = True

        if self.button_pressed and not self.sound_1_effect_played:
            game_loader.Audio.CONFIRM_MENU.play()
            self.sound_1_effect_played = True
            
    def custom_fade_in(self):
        self.alpha -= 3
        self.surf.set_alpha(self.alpha)
        game_loader.DisplaySurf.Screen.blit(self.surf, (0, 0))
        

    def reset_attr(self):
        super().reset_attr()
        self.sound_1_effect_played = self.sound_2_effect_played = self.button_pressed = False




class MenuScreen(Scene):
    def __init__(self):
        super().__init__()
        self.redirect = None
        self.redirect_delay = 1000
        
        self.week_score = 0
        
        self.top_rectangle = Surface(game_loader.DisplaySurf.WIDTH/2, 150, game_loader.DisplaySurf.WIDTH - 150, 200, (249, 209, 81))
        self.choose_your_track = game_loader.Font.TITLE_FONT_2.render("CHOOSE YOUR TRACK", True, "Black")
        self.cyt_rect = self.choose_your_track.get_rect(center = self.top_rectangle.rect.center)
        self.score_text = game_loader.Font.MENU_SCORE.render(f"SCORE: {self.week_score}", True, "White")
        self.st_rect = self.score_text.get_rect(midleft = (self.top_rectangle.rect.midleft[0], 25))


        self.some_rectangle = Surface(game_loader.DisplaySurf.WIDTH/2, 470, 270, 300)
        self.pointer = ImageAnimation(game_loader.Gallery.POINTER, self.some_rectangle.rect.centerx + 250, self.some_rectangle.rect.centery, 0.1)
        self.tracks = description_parser(file_parser())
        
    
    def draw_tracks(self):
        distance = 0
    
        for track in self.tracks:
            track.init_rect_coordinates(self.some_rectangle.rect.centerx, self.some_rectangle.rect.centery + distance)
            game_loader.DisplaySurf.Screen.blit(track.display_name, track.display_name_rect)
            distance += 100
    
    def redraw(self):
        game_loader.DisplaySurf.Screen.blit(self.top_rectangle.surface, self.top_rectangle.rect)
        game_loader.DisplaySurf.Screen.blit(self.choose_your_track, self.cyt_rect)
        game_loader.DisplaySurf.Screen.blit(self.score_text, self.st_rect)
        
        self.pointer.toggle_animation()
        
        self.draw_tracks()
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.redirect = "start screen"