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

        self.left_arrow_rect = self.left_arrow.get_rect(midleft=(self.rect.midleft[0] + 25, self.rect.midleft[1]))
        self.down_arrow_rect = self.down_arrow.get_rect(midleft=(self.rect.midleft[0] + 135, self.rect.midleft[1]))
        self.up_arrow_rect = self.up_arrow.get_rect(midright=(self.rect.midright[0] - 135, self.rect.midright[1]))
        self.right_arrow_rect = self.right_arrow.get_rect(midright=(self.rect.midright[0] - 25, self.rect.midright[1]))
        
        self.arrow_list = (
            (self.left_arrow, self.left_arrow_rect),
            (self.up_arrow, self.up_arrow_rect),
            (self.down_arrow, self.down_arrow_rect),
            (self.right_arrow, self.right_arrow_rect)
        )

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

        for object in self.arrow_list:
            ds.screen.blit(object[0], object[1])

    def event_on_arrow_deactivate(self, event):
        match event.key:
            case pg.K_UP:
                self.up_arrow = assets.Gallery.UP_ARROW

            case pg.K_DOWN:
                self.down_arrow = assets.Gallery.DOWN_ARROW

            case pg.K_LEFT:
                self.left_arrow = assets.Gallery.LEFT_ARROW

            case pg.K_RIGHT:
                self.right_arrow = assets.Gallery.RIGHT_ARROW