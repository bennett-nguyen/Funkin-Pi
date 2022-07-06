import pygame
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
from source.load.comp import Surface
from source.load.shared import shared_data

pygame.init()

class FlyingObject(Surface):
    def __init__(self, x: int, y: int, arrow, VEL) -> None:
        super().__init__(x, y, const.WIDTH/(13/5), 70)
        self.VEL = VEL
        self.arrow = arrow

        match self.arrow:
            case assets.Gallery.ACTIVATED_LEFT_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midleft=(self.rect.midleft[0] + 25, self.rect.midleft[1]))
                self.key = pygame.K_LEFT

            case assets.Gallery.ACTIVATED_DOWN_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midleft=(self.rect.midleft[0] + 135, self.rect.midleft[1]))
                self.key = pygame.K_DOWN

            case assets.Gallery.ACTIVATED_UP_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midright=(self.rect.midright[0] - 135, self.rect.midleft[1]))
                self.key = pygame.K_UP

            case assets.Gallery.ACTIVATED_RIGHT_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midright=(self.rect.midright[0] - 25, self.rect.midright[1]))
                self.key = pygame.K_RIGHT

    def draw_self(self):
        ds.screen.blit(self.arrow, self.arrow_rect)

    def move(self):
        self.rect.y -= round(self.VEL * shared_data.dt)
        self.arrow_rect.y -= round(self.VEL * shared_data.dt)

    def collide(self, object):
        # range from object.rect.center[1] + range --> object.rect.center[1] - range
        # the shorter the range, the harder you'll get a sick move
        range = 8
        target = self.rect
        lowest_center_range = object.rect.center[1] - range
        highest_center_range = object.rect.center[1] + range

        if target.center[1] >= lowest_center_range and target.center[1] <= highest_center_range and target.colliderect(object.rect):
            return (True, 'sick', const.SICK_EARNED)
        elif target.colliderect(object.rect):
            return (True, 'good', const.GOOD_EARNED)
        else:
            return [False]

    # this method is only used for the enemy!
    def collide_for_enemy(self, object):
        return self.rect.center[1] <= object.rect.center[1] and self.rect.colliderect(object)