import pygame
import load.game_loader as game_loader
import game.component
import general_component.component as genc

pygame.init()


class Track:
    def __init__(self, name: str, difficulties: list[str], score: dict, difficulties_config: dict, mapping: dict, soundtrack: dict, player_animation_path: dict):
        self.name = name
        display_name_font = game_loader.CustomFont.get_font("phantommuff-empty", 75)
        
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
        self.player_animation_path = player_animation_path
        self.player_entity = game.component.Entity(True, player_animation_path)

    def init_display_name_rect_coordinates(self, x, y):
        self.display_name_rect = self.display_name.get_rect(center=(x, y))
        self.display_name_animation = genc.ImageAnimation(
            (self.display_name, self.display_name_on_toggle), self.display_name_rect.centerx, self.display_name_rect.centery, 0.3)
    
    def run_init(self):
        self._mapping_to_objects()
        self._load_audio()

    def set_animation_coordinates(self, x, y):
        self.display_name_animation.rect.centerx = x
        self.display_name_animation.rect.centery = y
        
    def _load_audio(self):
        self.instrument = pygame.mixer.Sound(self.soundtrack_path["instrument"])
        self.vocal = pygame.mixer.Sound(self.soundtrack_path["vocal"])

    def _mapping_to_objects(self):
        self.objects = {}

        for diff, instruction in self.mapping.items():
            space = self.difficulties_config[diff]["space"]
            
            self.objects[diff] = []

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

        player_surface_x = (game_loader.DisplaySurf.WIDTH/4)*3
        enemy_surface_x = game_loader.DisplaySurf.WIDTH/4
        temp_dist = 0

        mapping_determiner_x = enemy_surface_x if "enemy" in name else player_surface_x if "player" in name else None

        for key in map:
            arrow = self.arrow_map.get(key, None)
            if arrow is None: continue
            self.objects[diff].append(
                game.component.FlyingObject(
                    mapping_determiner_x, game_loader.DisplaySurf.HEIGHT + space + temp_dist,
                    arrow,
                    velocity
                ))
            temp_dist += space

    def _load_side_stuff(self):
        text_font = game_loader.CustomFont.get_font("phantommuff-empty", 75)

        self.arrow_map = {
            "l": game_loader.Gallery.ACTIVATED_LEFT_ARROW,
            "r": game_loader.Gallery.ACTIVATED_RIGHT_ARROW,
            "u": game_loader.Gallery.ACTIVATED_UP_ARROW,
            "d": game_loader.Gallery.ACTIVATED_DOWN_ARROW,
        }

        self.easy_text = text_font.render(
            "EASY", True, (19, 253, 0))
        self.normal_text = text_font.render(
            "NORMAL", True, (242, 253, 0))
        self.hard_text = text_font.render(
            "HARD", True, (255, 0, 0))

        self.easy_text_rect = self.easy_text.get_rect(midleft=(900, 470))
        self.normal_text_rect = self.normal_text.get_rect(midleft=(900, 470))
        self.hard_text_rect = self.hard_text.get_rect(midleft=(900, 470))