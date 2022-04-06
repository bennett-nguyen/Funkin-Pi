import pygame
import load.game_loader as game_loader

pygame.init()

class Track:
    def __init__(self, name: str, difficulties: list[str], score: dict):
        self.display_name = game_loader.Font.TITLE_FONT_2.render(
            name.upper(), True, (255, 255, 255))

        self.difficulties = [
            game_loader.Font.TITLE_FONT_2.render(difficulty.upper(), True, (255, 255, 255))
            for difficulty in difficulties
            if difficulty.lower() in ["easy", "normal"]
        ]
        self.score = score
        
        self.alpha = 255
        self.display_name.set_alpha(self.alpha)
        
    def move_up(self):
        self.display_name_rect.y -= 100
    
    def move_down(self):
        self.display_name_rect.y += 100
        
    def init_rect_coordinates(self, x, y):
        self.display_name_rect = self.display_name.get_rect(center = (x, y))