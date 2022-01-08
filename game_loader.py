"""
Load all of the resources for this game and initialize the display surface
"""
import pygame

pygame.init()



class DisplaySurf:
    WIDTH = 1000
    HEIGHT = 675
    FPS = 60

    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Images
_scale = 2  # Increase this to get smaller arrow images

_LEFT_ARROW = pygame.image.load("./assets/left_arrow.png").convert_alpha()
_RIGHT_ARROW = pygame.image.load("./assets/right_arrow.png").convert_alpha()
_UP_ARROW = pygame.image.load("./assets/up_arrow.png").convert_alpha()
_DOWN_ARROW = pygame.image.load("./assets/down_arrow.png").convert_alpha()

_ACTIVATED_LEFT_ARROW = pygame.image.load(
    "./assets/activated_left_arrow.png").convert_alpha()

_ACTIVATED_RIGHT_ARROW = pygame.image.load(
    "./assets/activated_left_arrow.png").convert_alpha()

_ACTIVATED_UP_ARROW = pygame.image.load(
    "./assets/activated_up_arrow.png").convert_alpha()

_ACTIVATED_DOWN_ARROW = pygame.image.load(
    "./assets/activated_down_arrow.png").convert_alpha()


class Image:
    LEFT_ARROW = pygame.transform.scale(
        _LEFT_ARROW, (_LEFT_ARROW.get_width() / _scale, _LEFT_ARROW.get_height() / _scale))

    RIGHT_ARROW = pygame.transform.scale(
        _RIGHT_ARROW, (_RIGHT_ARROW.get_width() / _scale, _RIGHT_ARROW.get_height() / _scale))

    UP_ARROW = pygame.transform.scale(
        _UP_ARROW, (_UP_ARROW.get_width() / _scale, _UP_ARROW.get_height() / _scale))

    DOWN_ARROW = pygame.transform.scale(
        _DOWN_ARROW, (_DOWN_ARROW.get_width() / _scale, _DOWN_ARROW.get_height() / _scale))



    ACTIVATED_LEFT_ARROW = pygame.transform.scale(_ACTIVATED_LEFT_ARROW, (
        _ACTIVATED_LEFT_ARROW.get_width() / _scale, _ACTIVATED_LEFT_ARROW.get_height() / _scale))

    ACTIVATED_RIGHT_ARROW = pygame.transform.scale(_ACTIVATED_RIGHT_ARROW, (
        _ACTIVATED_RIGHT_ARROW.get_width() / _scale, _ACTIVATED_RIGHT_ARROW.get_height() / _scale))

    ACTIVATED_UP_ARROW = pygame.transform.scale(
        _ACTIVATED_UP_ARROW, (_ACTIVATED_UP_ARROW.get_width() / _scale, _ACTIVATED_UP_ARROW.get_height() / _scale))

    ACTIVATED_DOWN_ARROW = pygame.transform.scale(_ACTIVATED_DOWN_ARROW, (
        _ACTIVATED_DOWN_ARROW.get_width() / _scale, _ACTIVATED_DOWN_ARROW.get_height() / _scale))


class Audio:
    pass
