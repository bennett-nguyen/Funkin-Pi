import cv2
import pygame as pg
import source.load.ds as ds
import source.load.constant as const
from source.load.comp import Surface

pg.init()


class Entity(Surface):
    def __init__(self, is_player: bool, video_path) -> None:
        x = const.HALF_WIDTH/2
        if is_player:
            x = (const.HALF_WIDTH/2)*3

        super().__init__(x, const.HALF_HEIGHT, const.HALF_WIDTH, const.HEIGHT)

        self.video_path = video_path
        self.state = cv2.VideoCapture(self.video_path["idle"])

    def animation_is_playable(self):
        success, _ = self.state.read()
        return success

    def change_animation(self, animation):
        '''
        animation type: idle, left, up, down, right
        '''
        self.state = cv2.VideoCapture(self.video_path[animation])

    def load_animation(self):
        success, frame = self.state.read()

        if not success:
            return

        self.animation_surf = pg.image.frombuffer(
            frame.tobytes(), frame.shape[1::-1], "BGR")
        self.animation_rect = self.animation_surf.get_rect(
            center=self.rect.center)

    def draw_self(self):
        ds.screen.blit(self.surface, self.rect)
        ds.screen.blit(self.animation_surf, self.animation_rect)