import pygame
import game_loader

pygame.init()

image_loader = game_loader.Image

player_x = (game_loader.DisplaySurf.WIDTH/2/2)*3
enemy_x = game_loader.DisplaySurf.WIDTH/2/2

class TransparentSurf:
    def __init__(self, x: int, y: int):
        image_loader = game_loader.Image

        self.surface = pygame.Surface([game_loader.DisplaySurf.WIDTH/2/1.3, 60], pygame.SRCALPHA, 32)
        #self.surface.fill('Red')
        self.rect = self.surface.get_rect(center=(x, y))

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

class FlyingSurf:
    VEL = 7
    def __init__(self, x: int, y: int, arrow: game_loader.Image) -> None:
        self.x = x
        self.y = y

        self.surface = pygame.Surface([game_loader.DisplaySurf.WIDTH/2/1.3, 60], pygame.SRCALPHA, 32)
        #self.surface.fill('Red')
        self.rect = self.surface.get_rect(center = (self.x, self.y))

        self.arrow = arrow

        match self.arrow:
            case game_loader.Image.ACTIVATED_LEFT_ARROW:
                self.arrow_rect = self.arrow.get_rect(midleft = (self.rect.midleft[0], self.y))
                self.key = pygame.K_LEFT

            case game_loader.Image.ACTIVATED_DOWN_ARROW:
                self.arrow_rect = self.arrow.get_rect(midleft =  (self.rect.midleft[0] + 100, self.y))
                self.key = pygame.K_DOWN

            case game_loader.Image.ACTIVATED_UP_ARROW:
                self.arrow_rect = self.arrow.get_rect(midright =  (self.rect.midright[0] - 100, self.y))
                self.key = pygame.K_UP

            case game_loader.Image.ACTIVATED_RIGHT_ARROW:
                self.arrow_rect = self.arrow.get_rect(midright =  (self.rect.midright[0], self.y))
                self.key = pygame.K_RIGHT

    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        game_loader.DisplaySurf.Screen.blit(self.arrow, self.arrow_rect)

    def move(self):
        self.rect.y -= self.VEL
        self.arrow_rect.y -= self.VEL

    def collide_at_center(self, object):
        return self.rect.center <= object.rect.center

    def collide(self, object):
        # range from object.rect.center[1] + range --> object.rect.center[1] - range
        # the shorter the range, the harder you'll get a sick move
        range = 8
        target = self.rect
        lowest_center_range = object.rect.center[1] - range
        highest_center_range = object.rect.center[1] + range

        if target.center[1] >= lowest_center_range and target.center[1] <= highest_center_range:
            print('sick')
            return True

        elif target.colliderect(object.rect):
            print('good')
            return True

    def get_key(self):
        return self.key
    
class Entity:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
        self.surface = pygame.Surface([game_loader.DisplaySurf.WIDTH / 2, game_loader.DisplaySurf.HEIGHT])
        self.surface.fill('Red')
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        
        self.state = image_loader.ENTITY_IDLE # idle
        self.state_rect = self.state.get_rect(center=(self.x, self.y))
    
    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        game_loader.DisplaySurf.Screen.blit(self.state, self.state_rect)
    
player_entity = Entity(player_x, game_loader.DisplaySurf.HEIGHT/2)

enemy_surface = TransparentSurf(game_loader.DisplaySurf.WIDTH/2/2, 100)
player_surface = TransparentSurf(player_x, 100)

flying_object = FlyingSurf(player_x, 875, image_loader.ACTIVATED_LEFT_ARROW)
flying_object_3 = FlyingSurf(player_x, 1000, image_loader.ACTIVATED_DOWN_ARROW)
flying_object_2 = FlyingSurf(player_x, 1125, image_loader.ACTIVATED_UP_ARROW)
flying_object_4 = FlyingSurf(player_x, 1250, image_loader.ACTIVATED_RIGHT_ARROW)

objects = [flying_object, flying_object_3, flying_object_2, flying_object_4]
