import pygame as pg
import source.load.assets as assets
import source.load.constant as const
from collections import namedtuple
from source.load.comp import ImageAnimation
from source.comp.other.entity import Entity
from source.comp.other.obj import FlyingObject

pg.init()


class Track:
    def __init__(self, name: str, difficulties: list[str], score: dict, difficulties_config: dict, mapping: dict, soundtrack: dict, animation: dict, healthbar: dict):
        self.name = name
        display_name_font = assets.CustomFont.get_font("phantommuff-empty", const.TITLE_SIZE_2)

        self.display_name = display_name_font.render(name.upper(), True, (255, 255, 255))
        self.display_name_on_toggle = display_name_font.render(name.upper(), True, (0, 255, 255))

        self.difficulties = {}
        self.available_difficulties = difficulties

        self._load_side_stuff()
        for string, text, rect in (
            ("easy", self.easy_text, self.easy_text_rect),
            ("normal", self.normal_text, self.normal_text_rect),
            ("hard", self.hard_text, self.hard_text_rect)
        ):
            if string not in difficulties:
                self.difficulties[string] = None
                continue

            self.difficulties[string] = (text, rect)

        self.score = {
            "easy": score.get("easy", 0),
            "normal": score.get("normal", 0),
            "hard": score.get("hard", 0)
        }
        self.difficulties_config = difficulties_config
        self.mapping = mapping

        self.soundtrack_path = soundtrack
        self.player_entity = Entity(True, animation['player_animation'])

        HBColors = namedtuple('RGB', ('player', 'enemy'))
        self.hbcolors = HBColors(healthbar['color']['player'], healthbar['color']['enemy'])

        hb_player_state = healthbar['state']['player_state']
        hb_player_state_scale = healthbar['state']['player_state']['scale']

        self.player_state_dict = self._init_state(hb_player_state, hb_player_state_scale)

    def init_display_name_rect_coordinates(self, x, y):
        self.display_name_rect = self.display_name.get_rect(center=(x, y))
        self.display_name_animation = ImageAnimation(
            (self.display_name, self.display_name_on_toggle), self.display_name_rect.centerx, self.display_name_rect.centery, 0.3)

    def run_init(self):
        self._mapping_to_objects()
        self._load_audio()

    def set_animation_coordinates(self, x, y):
        self.display_name_animation.rect.centerx = x
        self.display_name_animation.rect.centery = y

    def _load_audio(self):
        self.instrument = pg.mixer.Sound(self.soundtrack_path["instrument"])
        self.vocal = pg.mixer.Sound(self.soundtrack_path["vocal"])

    def _mapping_to_objects(self):
        self.objs = {}

        for diff, instruction in self.mapping.items():
            space = self.difficulties_config[diff]["space"]

            self.objs[diff] = []

            for name, map in instruction.items():
                if "enemy" in name or "player" in name:
                    self._enemy_n_player_mapping(name, diff, space, map, self.difficulties_config[diff]["velocity"])

                elif "set" in name and map.startswith("$"):
                    match map[1:map.find(":")]:
                        case "space":
                            space = int(map[map.find(":")+1:])
                        case "reset":
                            space = self.difficulties_config[diff]["space"]

    def _enemy_n_player_mapping(self, name, diff, space, map, velocity):
        temp_dist = 0

        mapping_determiner_x = const.ENEMY_ARROW_SET_X if "enemy" in name else const.PLAYER_ARROW_SET_X if "player" in name else None

        for key in map:
            arrow = self.arrow_map.get(key, None)
            if arrow is None:
                continue
            self.objs[diff].append(
                FlyingObject(
                    mapping_determiner_x, const.HEIGHT + space + temp_dist,
                    arrow,
                    velocity
                ))
            temp_dist += space

    def _load_side_stuff(self):
        text_font = assets.CustomFont.get_font("phantommuff-empty", const.TITLE_SIZE_2)

        self.arrow_map = {
            "l": assets.Gallery.ACTIVATED_LEFT_ARROW,
            "r": assets.Gallery.ACTIVATED_RIGHT_ARROW,
            "u": assets.Gallery.ACTIVATED_UP_ARROW,
            "d": assets.Gallery.ACTIVATED_DOWN_ARROW,
        }

        self.easy_text = text_font.render("EASY", True, (19, 253, 0))
        self.normal_text = text_font.render("NORMAL", True, (242, 253, 0))
        self.hard_text = text_font.render("HARD", True, (255, 0, 0))

        self.easy_text_rect = self.easy_text.get_rect(midleft=(900, 470))
        self.normal_text_rect = self.normal_text.get_rect(midleft=(900, 470))
        self.hard_text_rect = self.hard_text.get_rect(midleft=(900, 470))

    def destruct_unnecessary_stuff(self):
        del self.easy_text
        del self.normal_text
        del self.hard_text
        del self.easy_text_rect
        del self.normal_text_rect
        del self.hard_text_rect
        del self.mapping
        del self.soundtrack_path
        del self.arrow_map

    def _init_state(self, hb_state: dict, scale: float) -> dict:
        state_dict = {}
        for label, path in hb_state.items():
            if label != 'scale':
                state = pg.transform.rotozoom(pg.image.load(path).convert_alpha(), 0, scale) if scale is not None else pg.image.load(path).convert_alpha()
                state_dict[label] = state
        return state_dict
