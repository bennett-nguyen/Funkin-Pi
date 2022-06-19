import pygame
import load.game_loader as game_loader
from typing import Callable

pygame.init()


class Surface:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int] = None, alpha: bool = False):
        self.surface = pygame.Surface(
            (width, height), pygame.SRCALPHA, 32) if alpha else pygame.Surface((width, height))

        if color is not None:
            self.surface.fill(color)

        self.rect = self.surface.get_rect(center=(x, y))


class ImageAnimation:
    def __init__(self, images: tuple, x: int, y: int, speed: float):
        self.images = images
        self.index = 0
        self.speed = speed  # 0 -> 1 high speed == fast animation

        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(center=(x, y))

    def toggle_animation(self):
        self.index += self.speed
        if self.index >= len(self.images):
            self.index = 0
        self.surf = self.images[int(self.index)]

        game_loader.DisplaySurf.Screen.blit(self.surf, self.rect)

class Button(Surface):
    def __init__(self, pos: tuple[int, int], hitbox_size: tuple[int, int], deactivation_assets, on_hover_assets, activation_assets = None, speed: tuple[int, int, int] = (0.1, 0.1, 0.1)):
        super().__init__(pos[0], pos[1], hitbox_size[0], hitbox_size[1], None, True)
        
        deactivation_state = ImageAnimation(deactivation_assets, self.rect.centerx, self.rect.centery, speed[0])
        on_hover_state = ImageAnimation(on_hover_assets, self.rect.centerx, self.rect.centery, speed[1])
        activation_state = ImageAnimation(activation_assets, self.rect.centerx, self.rect.centery, speed[2]) if activation_assets is not None else None

        self.animation_list = [deactivation_state, on_hover_state, activation_state]

        self.activated_by_click = False
        self.activated_by_key = False
        self.is_on_hover = False

    def toggle_animation(self, animation_type: int):
        """
        animation_type:
            - 0: deactivation animation
            - 1: on hover animation
            - 2: activation animation
        """
        self.animation_list[animation_type].toggle_animation()

    def check_click(self, click_type: int):
        '''
        click_type:
            - 0: left click
            - 1: middle click
            - 2: right click
        '''
        self.check_hover()
        self.activated_by_click = self.is_on_hover and pygame.mouse.get_pressed()[click_type]

    def check_key_activate(self, key):
        keys = pygame.key.get_pressed()
        self.activated_by_key = keys[key]

    def check_hover(self):
        self.is_on_hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def deactivate_button(self, deactivate_type: int):
        """
        0: both activated_by_click and activated_by_key
        1: activated_by_click
        2: activated_by_key
        """
        match deactivate_type:
            case 0:
                self.activated_by_click = self.activated_by_key = False
            case 1:
                self.activated_by_click = False
            case 2:
                self.activated_by_key = False
    
    def is_activated(self, check_type: int):
        """
        0: both is_activated_by_click and activated_by_key
        1: activated_by_click or activated_by_key
        2: activated_by_click
        3: activated_by_key
        """
        match check_type:
            case 0:
                return self.activated_by_click and self.activated_by_key
            case 1:
                return self.activated_by_click or self.activated_by_key
            case 2:
                return self.activated_by_click
            case 3:
                return self.activated_by_key