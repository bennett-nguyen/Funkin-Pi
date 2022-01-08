import pygame
import game_loader

pygame.init()


class TransparentSurf:
    def __init__(self, x, y):
        image_loader = game_loader.Image
        # , pygame.SRCALPHA, 32)

        self.surface = pygame.Surface([game_loader.DisplaySurf.WIDTH/2/1.3, 100], pygame.SRCALPHA, 32)
        self.rect = self.surface.get_rect(center=(x, y))
        
        self.left_arrow = image_loader.LEFT_ARROW
        self.up_arrow = image_loader.UP_ARROW
        self.down_arrow = image_loader.DOWN_ARROW
        self.right_arrow = image_loader.RIGHT_ARROW

        self.left_arrow_rect = self.left_arrow.get_rect(midleft = self.rect.midleft)
        self.up_arrow_rect = self.up_arrow.get_rect(midleft = (self.rect.midleft[0] + 100, self.rect.midleft[1]))
        self.down_arrow_rect = self.down_arrow.get_rect(midright = (self.rect.midright[0] - 100, self.rect.midleft[1]))
        self.right_arrow_rect = self.right_arrow.get_rect(midright = self.rect.midright)
    def draw_arrow(self):

        game_loader.DisplaySurf.Screen.blit(self.left_arrow, self.left_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(self.up_arrow, self.up_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(self.down_arrow, self.down_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(self.right_arrow, self.right_arrow_rect)

class FlyingSurf:
    def __init__(self, y, arrow):
        self.x = game_loader.DisplaySurf.WIDTH/2/2
        self.y = y

        self.surface = pygame.Surface([game_loader.DisplaySurf.WIDTH/2/1.3, 100], pygame.SRCALPHA, 32)
        self.rect = self.surface.get_rect(center = (self.x, self.y))

        self.arrow = arrow 
        
        match arrow:
            case game_loader.Image.LEFT_ARROW:
                self.arrow_rect = self.arrow.get_rect(midleft = (self.rect.midleft[0], self.y))
                self.key = 'left'
            case game_loader.Image.UP_ARROW:
                self.arrow_rect = self.arrow.get_rect(midleft =  (self.rect.midleft[0] + 100, self.y))
                self.key = 'up'
            case game_loader.Image.DOWN_ARROW:
                self.arrow_rect = self.arrow.get_rect(midright =  (self.rect.midright[0] - 100, self.y))
                self.key = 'down'
            case game_loader.Image.RIGHT_ARROW:
                self.arrow_rect = self.arrow.get_rect(midright =  (self.rect.midright[0], self.y))    
                self.key = 'right'

    def draw_arrow(self):
        game_loader.DisplaySurf.Screen.blit(self.arrow, self.arrow_rect)
    
    def move(self):
        self.rect.y -= 5

    def move_arrow(self):
        self.arrow_rect.y -= 5




transparent_rect = TransparentSurf(game_loader.DisplaySurf.WIDTH/2/2, 80)
transparent_rect2 = TransparentSurf((game_loader.DisplaySurf.WIDTH/2/2)*3, 80)

flying_object = FlyingSurf(875, game_loader.Image.LEFT_ARROW)
flying_object_2 = FlyingSurf(1000, game_loader.Image.UP_ARROW)
flying_object_3 = FlyingSurf(1125, game_loader.Image.DOWN_ARROW)
flying_object_4 = FlyingSurf(1250, game_loader.Image.RIGHT_ARROW)

objects = [flying_object, flying_object_2, flying_object_3, flying_object_4]
