import pygame
from dataclasses import dataclass

pygame.init()

@dataclass(eq=False, unsafe_hash=False)
class __SharedData:
    """
    Defines the data that will be shared across all components
    """
    dt: float
    events: pygame.event

shared_data = __SharedData(None, None)