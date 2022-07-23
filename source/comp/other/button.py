import pygame as pg
from source.load.comp import ImageAnimation, Surface

pg.init()


class Button(Surface):
    def __init__(self, pos: tuple[int, int], hitbox_size: tuple[int, int], deactivation_assets, on_hover_assets, activation_assets=None, speed: tuple[int, int, int] = (0.1, 0.1, 0.1)):
        x, y = pos
        hw, hh = hitbox_size
        super().__init__(x, y, hw, hh, None, True)

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
        self.activated_by_click = self.is_on_hover and pg.mouse.get_pressed()[click_type]

    def check_key_activate(self, key):
        keys = pg.key.get_pressed()
        self.activated_by_key = keys[key]

    def check_hover(self):
        self.is_on_hover = self.rect.collidepoint(pg.mouse.get_pos())

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