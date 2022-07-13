import pygame
import source.load.ds as ds

pygame.init()

class Surface:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int] = None, alpha: bool = False):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) if alpha else pygame.Surface((width, height))
        self.rect = self.surface.get_rect(center=(x, y))
        
        if color is not None: self.surface.fill(color)



class ImageAnimation:
    def __init__(self, images: tuple, x: int, y: int, speed: float):
        self.images = images
        self.index = 0
        self.speed = speed  # 0 -> 1 high speed == fast animation

        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(center=(x, y))

    def toggle_animation(self):
        self.index += self.speed
        if self.index >= len(self.images): self.index = 0

        self.surf = self.images[int(self.index)]
        ds.screen.blit(self.surf, self.rect)