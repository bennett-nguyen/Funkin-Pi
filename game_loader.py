"""
Load all of the resources for this game and initialize the display surface
"""
import pygame

pygame.init()
pygame.mixer.init()


class DisplaySurf:
    WIDTH = 1000
    HEIGHT = 675
    FPS = 60

    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Video animation must be 500x675px

# Images
_scale = 2  # Increase this to get smaller arrow images

_LEFT_ARROW = pygame.image.load("./assets/img/left_arrow.png").convert_alpha()
_RIGHT_ARROW = pygame.image.load("./assets/img/right_arrow.png").convert_alpha()
_UP_ARROW = pygame.image.load("./assets/img/up_arrow.png").convert_alpha()
_DOWN_ARROW = pygame.image.load("./assets/img/down_arrow.png").convert_alpha()

_ACTIVATED_LEFT_ARROW = pygame.image.load(
    "./assets/img/activated_left_arrow.png").convert_alpha()

_ACTIVATED_RIGHT_ARROW = pygame.image.load(
    "./assets/img/activated_right_arrow.png").convert_alpha()

_ACTIVATED_UP_ARROW = pygame.image.load(
    "./assets/img/activated_up_arrow.png").convert_alpha()

_ACTIVATED_DOWN_ARROW = pygame.image.load(
    "./assets/img/activated_down_arrow.png").convert_alpha()

_IDLE = pygame.image.load('./assets/img/idle.png').convert_alpha()
_UP = pygame.image.load('./assets/img/up.png').convert_alpha()
_DOWN = pygame.image.load('./assets/img/down.png').convert_alpha()
_LEFT = pygame.image.load('./assets/img/left.png').convert_alpha()
_RIGHT = pygame.image.load('./assets/img/right.png').convert_alpha()

_SOUTH_INSTRUMENT = pygame.mixer.Sound("./assets/audio/south_instrument.mp3")
_SOUTH_VOCAL = pygame.mixer.Sound('./assets/audio/south_vocal.mp3')


class Image:
    LEFT_ARROW = pygame.transform.scale(
        _LEFT_ARROW, (_LEFT_ARROW.get_width() / _scale, _LEFT_ARROW.get_height() / _scale))

    RIGHT_ARROW = pygame.transform.scale(
        _RIGHT_ARROW, (_RIGHT_ARROW.get_width() / _scale, _RIGHT_ARROW.get_height() / _scale))

    UP_ARROW = pygame.transform.scale(
        _UP_ARROW, (_UP_ARROW.get_width() / _scale, _UP_ARROW.get_height() / _scale))

    DOWN_ARROW = pygame.transform.scale(
        _DOWN_ARROW, (_DOWN_ARROW.get_width() / _scale, _DOWN_ARROW.get_height() / _scale))

    ENTITY_IDLE = _IDLE
    ENTITY_UP = _UP
    ENTITY_DOWN = _DOWN
    ENTITY_LEFT = _LEFT
    ENTITY_RIGHT = _RIGHT

    ACTIVATED_LEFT_ARROW = pygame.transform.scale(_ACTIVATED_LEFT_ARROW, (
        _ACTIVATED_LEFT_ARROW.get_width() / _scale, _ACTIVATED_LEFT_ARROW.get_height() / _scale))

    ACTIVATED_RIGHT_ARROW = pygame.transform.scale(_ACTIVATED_RIGHT_ARROW, (
        _ACTIVATED_RIGHT_ARROW.get_width() / _scale, _ACTIVATED_RIGHT_ARROW.get_height() / _scale))

    ACTIVATED_UP_ARROW = pygame.transform.scale(
        _ACTIVATED_UP_ARROW, (_ACTIVATED_UP_ARROW.get_width() / _scale, _ACTIVATED_UP_ARROW.get_height() / _scale))

    ACTIVATED_DOWN_ARROW = pygame.transform.scale(_ACTIVATED_DOWN_ARROW, (
        _ACTIVATED_DOWN_ARROW.get_width() / _scale, _ACTIVATED_DOWN_ARROW.get_height() / _scale))

class Audio:
    INSTRUMENT = _SOUTH_INSTRUMENT
    VOCAL = _SOUTH_VOCAL
    
    VOCAL_VOLUME = 1