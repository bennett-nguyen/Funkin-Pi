import pygame as pg
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
from source.load.comp import Surface
from source.load.shared import shared_data

pg.init()


class FlyingObject(Surface):
    def __init__(self, x: int, y: int, arrow, VEL: int):
        super().__init__(x, y, const.WIDTH/(13/5), 65, (255, 255, 255))
        self.VEL = VEL
        self.arrow = arrow
        self.score_earned = 0
        self.message = None
        self.disabled = False

        match self.arrow:
            case assets.Gallery.ACTIVATED_LEFT_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midleft=(self.rect.left + 25, self.rect.centery))
                self.key = pg.K_LEFT

            case assets.Gallery.ACTIVATED_DOWN_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midleft=(self.rect.left + 135, self.rect.centery))
                self.key = pg.K_DOWN

            case assets.Gallery.ACTIVATED_UP_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midright=(self.rect.right - 135, self.rect.centery))
                self.key = pg.K_UP

            case assets.Gallery.ACTIVATED_RIGHT_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midright=(self.rect.right - 25, self.rect.centery))
                self.key = pg.K_RIGHT

    def draw_self(self):
        # ds.screen.blit(self.surface, self.rect) # un-comment this to reveal hitbox
        ds.screen.blit(self.arrow, self.arrow_rect)

    def move(self):
        self.rect.y -= round(self.VEL * shared_data.dt)
        self.arrow_rect.y -= round(self.VEL * shared_data.dt)

    def collide(self, arrow_set) -> str:
        is_colliding = self.rect.colliderect(arrow_set.rect)
        if not is_colliding:
            self.message = 'bad'
            self.score_earned = 0
            return
        
        collide_type, score_earned = arrow_set.check_collide_type(self.rect.centery)
        self.message = collide_type
        self.score_earned = score_earned

    def disable_obj(self):
        self.disabled = True

    # this method is only used for the enemy!
    def collide_for_enemy(self, arrow_set):
        return self.rect.centery <= arrow_set.rect.centery and self.rect.colliderect(arrow_set)