import pygame
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const

from source.load.template import Scene
from source.load.shared import shared_data
from source.comp.other.menu_comp import MenuLogic
from source.load.comp import Surface, ImageAnimation
from source.comp.json.load import data_parser, file_parser

pygame.init()

class MenuScreen(Scene):
    def __init__(self):
        super().__init__()
        title_font_2 = assets.CustomFont.get_font("phantommuff-empty", const.TITLE_SIZE_2)
        self.redirect_delay = 3500
        self.fade_delay = 2400
        self.on_toggle_chosen_track = False

        self.yellow_rectangle = Surface(const.HALF_WIDTH, 150, const.WIDTH - 150, 200, (249, 209, 81))

        self.choose_your_track = title_font_2.render("CHOOSE YOUR TRACK", True, "Black")
        self.cyt_rect = self.choose_your_track.get_rect(center=self.yellow_rectangle.rect.center)

        self.track_chooser_rect = Surface(const.HALF_WIDTH, 470, 270, 300)
        self.pointer = ImageAnimation(assets.Gallery.POINTER, self.track_chooser_rect.rect.centerx + 250, self.track_chooser_rect.rect.centery, 0.1)
        self.tracks = data_parser(file_parser())

        distance = 0

        for track in self.tracks:
            track.init_display_name_rect_coordinates(self.track_chooser_rect.rect.centerx, self.track_chooser_rect.rect.centery + distance)
            track.run_init()
            track.destruct_unnecessary_stuff()
            distance += 120

        self.logic = MenuLogic(self.tracks)

    def redraw(self):
        self.logic.redraw()

        ds.screen.blit(self.yellow_rectangle.surface, self.yellow_rectangle.rect)
        ds.screen.blit(self.choose_your_track, self.cyt_rect)

        self.pointer.toggle_animation()

        if self.on_toggle_chosen_track:
            self.logic.current_track.display_name_animation.toggle_animation()

    def input(self):
        if self.allow_keydown:
            self.logic.input()

            for event in shared_data.events:
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.redirect = "start screen"
                            self.allow_keydown = False

                        case pygame.K_RETURN:
                            self._key_return_event()

    def _key_return_event(self):
        self.loaded_data = self.logic.load_track_data()
        self.logic.current_track.set_animation_coordinates(
            self.logic.current_track.display_name_rect.centerx,
            self.logic.current_track.display_name_rect.centery
        )

        assets.Audio.CONFIRM_MENU.play()
        self.on_toggle_chosen_track = True
        self.redirect = "main game"
        self.allow_keydown = False

    def reset_attr(self):
        super().reset_attr()
        self.loaded_data = None