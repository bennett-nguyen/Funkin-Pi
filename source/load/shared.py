import pygame
from dataclasses import dataclass

pygame.init()

@dataclass
class _SharedData:
    """
    Defines the data that will be shared across all components
    """
    dt: float
    events: pygame.event

shared_data = _SharedData(None, None)