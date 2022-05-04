import pygame
import load.game_loader as game_loader
import game.component
import general_component.component as genc

pygame.init()


class Track:
    def __init__(self, name: str, difficulties: list[str], score: dict, difficulties_config: dict, mapping: dict):
        self.name = name
        self.display_name = game_loader.Font.TITLE_FONT_2.render(
            name.upper(), True, (255, 255, 255))

        self.display_name_on_toggle = game_loader.Font.TITLE_FONT_2.render(
            name.upper(), True, (0, 255, 255))

        easy_text = game_loader.Font.TITLE_FONT_2.render(
            "EASY", True, (19, 253, 0))
        normal_text = game_loader.Font.TITLE_FONT_2.render(
            "NORMAL", True, (242, 253, 0))
        hard_text = game_loader.Font.TITLE_FONT_2.render(
            "HARD", True, (255, 0, 0))

        easy_text_rect = easy_text.get_rect(midleft=(900, 470))
        normal_text_rect = normal_text.get_rect(midleft=(900, 470))
        hard_text_rect = hard_text.get_rect(midleft=(900, 470))

        self.difficulties = {}
        self.available_difficulties = difficulties

        for i in (("easy", easy_text, easy_text_rect), ("normal", normal_text, normal_text_rect), ("hard", hard_text, hard_text_rect)):
            if i[0] not in difficulties:
                self.difficulties[i[0]] = None
                continue

            self.difficulties[i[0]] = (i[1], i[2])

        self.score = {
            "easy": score.get("easy", 0),
            "normal": score.get("normal", 0),
            "hard": score.get("hard", 0)
        }
        self.difficulties_config = difficulties_config
        self.mapping = mapping

    def mapping_to_objects(self):
        self.objects = {}
        
        player_surface_x = (game_loader.DisplaySurf.WIDTH/2/2)*3
        enemy_surface_x = game_loader.DisplaySurf.WIDTH/2/2

        for diff, instruction in self.mapping.items():
            space = self.difficulties_config[diff]["space"]
            velocity = self.difficulties_config[diff]["velocity"]
            
            self.objects[diff] = []

            game.component.FlyingObject.VEL = velocity
            temp_dist = 0

            for name, map in instruction.items():
                if "enemy" in name:
                    for key in map:
                        arrow = game_loader.Gallery.ACTIVATED_LEFT_ARROW if key == 'l' else game_loader.Gallery.ACTIVATED_RIGHT_ARROW if key == 'r' else game_loader.Gallery.ACTIVATED_UP_ARROW if key == 'u' else game_loader.Gallery.ACTIVATED_DOWN_ARROW if key == 'd' else None
                        if arrow is None:
                            continue
                        self.objects[diff].append(game.component.FlyingObject(
                            enemy_surface_x, game_loader.DisplaySurf.HEIGHT + space + temp_dist, arrow))
                        temp_dist += space

                elif "player" in name:
                    for key in map:
                        arrow = game_loader.Gallery.ACTIVATED_LEFT_ARROW if key == 'l' else game_loader.Gallery.ACTIVATED_RIGHT_ARROW if key == 'r' else game_loader.Gallery.ACTIVATED_UP_ARROW if key == 'u' else game_loader.Gallery.ACTIVATED_DOWN_ARROW if key == 'd' else None
                        if arrow is None:
                            continue
                        self.objects[diff].append(game.component.FlyingObject(
                            player_surface_x, game_loader.DisplaySurf.HEIGHT + space + temp_dist, arrow))
                        temp_dist += space

                elif "set" in name and map.startswith("$"):
                    match map[1:map.find(":")]:
                        case "space":
                            space = int(map[map.find(":")+1:])
                        case "reset":
                            space = self.difficulties_config[diff]["space"]

    def init_display_name_rect_coordinates(self, x, y):
        
        self.display_name_rect = self.display_name.get_rect(center=(x, y))
        self.display_name_animation = genc.ImageAnimation(
            (self.display_name, self.display_name_on_toggle), self.display_name_rect.centerx, self.display_name_rect.centery, 0.3)
    
    def run_init(self):
        self.mapping_to_objects()
        
    def set_animation_coordinates(self, x, y):
        self.display_name_animation.rect.centerx = x
        self.display_name_animation.rect.centery = y