import pygame as pg
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
from source.load.comp import Surface

pg.init()


class ArrowSet(Surface):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, const.HALF_WIDTH/1.3, 65, (255, 255, 255))

        self.left_arrow = assets.Gallery.LEFT_ARROW
        self.up_arrow = assets.Gallery.UP_ARROW
        self.down_arrow = assets.Gallery.DOWN_ARROW
        self.right_arrow = assets.Gallery.RIGHT_ARROW

        self.left_arrow_rect = self.left_arrow.get_rect(midleft=(self.rect.left + 25, self.rect.centery))
        self.down_arrow_rect = self.down_arrow.get_rect(midleft=(self.rect.left + 135, self.rect.centery))
        self.up_arrow_rect = self.up_arrow.get_rect(midright=(self.rect.right - 135, self.rect.centery))
        self.right_arrow_rect = self.right_arrow.get_rect(midright=(self.rect.right - 25, self.rect.centery))

        self.arrow_list = (
            (self.left_arrow, self.left_arrow_rect),
            (self.up_arrow, self.up_arrow_rect),
            (self.down_arrow, self.down_arrow_rect),
            (self.right_arrow, self.right_arrow_rect)
        )

        sick_range = 8
        self.lowest = self.rect.centery - sick_range
        self.highest = self.rect.centery + sick_range


    def update_arrows(self):
        self.arrow_list = (
            (self.left_arrow, self.left_arrow_rect),
            (self.up_arrow, self.up_arrow_rect),
            (self.down_arrow, self.down_arrow_rect),
            (self.right_arrow, self.right_arrow_rect)
        )

    def draw_self(self):
        # ds.screen.blit(self.surface, self.rect) # un-comment this to reveal hitbox
        self.update_arrows()

        for obj in self.arrow_list:
            ds.screen.blit(obj[0], obj[1])

    def event_on_arrow_deactivate(self, key):
        match key:
            case pg.K_UP:
                self.up_arrow = assets.Gallery.UP_ARROW

            case pg.K_DOWN:
                self.down_arrow = assets.Gallery.DOWN_ARROW

            case pg.K_LEFT:
                self.left_arrow = assets.Gallery.LEFT_ARROW

            case pg.K_RIGHT:
                self.right_arrow = assets.Gallery.RIGHT_ARROW
    
    def check_collide_type(self, cy):
        # you'll get a sick move if you press the key at the moment
        # when the centery coordinate of the object (reference as: cy) met the following condition: lowest <= cy <= highest
        if self.lowest <= cy <= self.highest:
            return ('sick', const.SICK_EARNED)
        return ('good', const.GOOD_EARNED)