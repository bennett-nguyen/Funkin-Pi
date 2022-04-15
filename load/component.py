import pygame
import itertools
import load.game_loader as game_loader

pygame.init()


def sort_difficulty(sort_order, array):
    return [
        string for order, string in itertools.product(sort_order, array) if string[0] == order
    ]


class Track:
    def __init__(self, name: str, difficulties: list[str], score: dict):
        self.display_name = game_loader.Font.TITLE_FONT_2.render(
            name.upper(), True, (255, 255, 255))

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

        for i in (("easy", easy_text, easy_text_rect), ("normal", normal_text, normal_text_rect), ("hard", hard_text, hard_text_rect)):
            if i[0] not in difficulties:
                self.difficulties[i[0]] = None
                continue

            self.difficulties[i[0]] = (i[1], i[2])

        self.available_difficulties = sort_difficulty(
            ("e", "n", "h"), 
            [difficulty for difficulty in difficulties if self.difficulties[difficulty] is not None]
            )

        self.score = {
            "easy": score.get("easy", 0),
            "normal": score.get("normal", 0),
            "hard": score.get("hard", 0)
        }

    def init_display_name_rect_coordinates(self, x, y):
        self.display_name_rect = self.display_name.get_rect(center=(x, y))
