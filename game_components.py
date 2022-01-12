import pygame
import game_loader

pygame.init()

image_loader = game_loader.Image


class Surface:
    def __init__(self, x, y, width, height):
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        #self.surface.fill('Red')
        self.rect = self.surface.get_rect(center=(x, y))
        
class TransparentSurf(Surface):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH/2/1.3, 60)

        self.left_arrow = image_loader.LEFT_ARROW
        self.up_arrow = image_loader.UP_ARROW
        self.down_arrow = image_loader.DOWN_ARROW
        self.right_arrow = image_loader.RIGHT_ARROW

        self.left_arrow_rect = self.left_arrow.get_rect(midleft = self.rect.midleft)
        self.down_arrow_rect = self.down_arrow.get_rect(midleft = (self.rect.midleft[0] + 100, self.rect.midleft[1]))
        self.up_arrow_rect = self.up_arrow.get_rect(midright = (self.rect.midright[0] - 100, self.rect.midright[1]))
        self.right_arrow_rect = self.right_arrow.get_rect(midright = self.rect.midright)

    def draw_arrow(self):
        game_loader.DisplaySurf.Screen.blit(self.left_arrow, self.left_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(self.up_arrow, self.up_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(self.down_arrow, self.down_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(self.right_arrow, self.right_arrow_rect)
    
    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        self.draw_arrow()
        
    def event_on_arrow_deactivate(self, event):
        match event.key:
            case pygame.K_UP:
                self.up_arrow = image_loader.UP_ARROW

            case pygame.K_DOWN:
                self.down_arrow = image_loader.DOWN_ARROW

            case pygame.K_LEFT:
                self.left_arrow = image_loader.LEFT_ARROW

            case pygame.K_RIGHT:
                self.right_arrow = image_loader.RIGHT_ARROW

class FlyingSurf(Surface):
    VEL = 7
    def __init__(self, x: int, y: int, arrow: game_loader.Image, is_player: bool = False) -> None:
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH/2/1.3, 60)

        self.arrow = arrow
        self.is_player = is_player
        
        match self.arrow:
            case game_loader.Image.ACTIVATED_LEFT_ARROW:
                self.arrow_rect = self.arrow.get_rect(midleft = self.rect.midleft)
                self.key = pygame.K_LEFT

            case game_loader.Image.ACTIVATED_DOWN_ARROW:
                self.arrow_rect = self.arrow.get_rect(midleft =  (self.rect.midleft[0] + 100, self.rect.midleft[1]))
                self.key = pygame.K_DOWN

            case game_loader.Image.ACTIVATED_UP_ARROW:
                self.arrow_rect = self.arrow.get_rect(midright =  (self.rect.midright[0] - 100, self.rect.midleft[1]))
                self.key = pygame.K_UP

            case game_loader.Image.ACTIVATED_RIGHT_ARROW:
                self.arrow_rect = self.arrow.get_rect(midright =  self.rect.midright)
                self.key = pygame.K_RIGHT

    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        game_loader.DisplaySurf.Screen.blit(self.arrow, self.arrow_rect)

    def move(self):
        self.rect.y -= self.VEL
        self.arrow_rect.y -= self.VEL

    # this collide method is only used for the enemy only!
    def collide_for_enemy(self, object):
        return self.rect.center[1] <= object.rect.center[1] and self.rect.colliderect(object)

    def collide(self, object):
        # range from object.rect.center[1] + range --> object.rect.center[1] - range
        # the shorter the range, the harder you'll get a sick move
        range = 8
        target = self.rect
        lowest_center_range = object.rect.center[1] - range
        highest_center_range = object.rect.center[1] + range

        if target.center[1] >= lowest_center_range and target.center[1] <= highest_center_range and target.colliderect(object.rect):
            print('sick')
            return True

        elif target.colliderect(object.rect):
            print('good')
            return True
    
class Entity(Surface):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH / 2, game_loader.DisplaySurf.HEIGHT)
        
        self.state = image_loader.ENTITY_IDLE
        self.state_rect = self.state.get_rect(center=self.rect.center)

    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        game_loader.DisplaySurf.Screen.blit(self.state, self.state_rect)