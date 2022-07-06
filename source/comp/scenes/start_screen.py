import pygame
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
from source.load.template import Scene
from source.comp.other.button import Button

pygame.init()

class StartScreen(Scene):
    def __init__(self):
        super().__init__()
        self.sound_1_effect_played = self.sound_2_effect_played = False

        self.redirect_delay = 3500
        self.fade_delay = 2500

        # custom fade in animation
        self.surf = pygame.Surface(ds.screen.get_size())
        self.surf.fill((255, 255, 255))

        self.alpha = 255
        # ----
        
        self.start_button = Button(
            (const.HALF_WIDTH, const.HALF_HEIGHT + 270),
            (250, 120),
            assets.Gallery.PLAY_BUTTON_DEACTIVATED_IMAGES,
            assets.Gallery.PLAY_BUTTON_ON_HOVER_IMAGES,
            assets.Gallery.PLAY_BUTTON_ACTIVATED_IMAGES
        )


    def redraw(self):
        ds.screen.blit(assets.Gallery.LOGO, assets.Gallery.LOGO.get_rect(center=(const.HALF_WIDTH, const.HALF_HEIGHT)))
        self.start_button.check_hover()

        if self.start_button.is_activated(check_type=1):
            self.start_button.toggle_animation(animation_type=2)
            self.redirect = "menu screen"

        elif self.start_button.is_on_hover:
            self.start_button.toggle_animation(animation_type=1)
            if not self.sound_2_effect_played:
                assets.Audio.SCROLL_MENU.play()
                self.sound_2_effect_played = True

        else:
            self.start_button.toggle_animation(animation_type=0)
            self.sound_2_effect_played = False

        if self.alpha > -1:
            self.custom_fade_in()

    def input(self):
        self.start_button.check_click(click_type=0)
        self.start_button.check_key_activate(key = pygame.K_RETURN)

        if self.start_button.is_activated(check_type=1) and not self.sound_1_effect_played:
            assets.Audio.CONFIRM_MENU.play()
            self.sound_1_effect_played = True

    def custom_fade_in(self):
        self.alpha -= 3
        self.surf.set_alpha(self.alpha)
        ds.screen.blit(self.surf, (0, 0))

    def reset_attr(self):
        super().reset_attr()
        self.sound_1_effect_played = self.sound_2_effect_played = False
        self.start_button.deactivate_button(0)