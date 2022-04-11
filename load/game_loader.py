"""
Load all of the resources for this game and initialize the display surface
"""
import pygame
from pygame.locals import *
import load.file_loader as file_loader

flags = FULLSCREEN | DOUBLEBUF

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])
pygame.display.set_caption("Funky Friday at Home")


class DisplaySurf:
    WIDTH = 1200
    HEIGHT = 690
    FPS = 60

    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))

# class Stat:
#     missed_counter = 0
#     hit_counter = 0

#     score = 0

#     def get_accuracy(self):
#         return self.hit_counter / (self.missed_counter + self.hit_counter) * 100

# Video animation must be 600x690px


# Images
_scale = 2  # Increase this to get smaller arrow images

_LEFT_ARROW = pygame.image.load(
    "./assets/img/left_arrow.png").convert_alpha()
_RIGHT_ARROW = pygame.image.load(
    "./assets/img/right_arrow.png").convert_alpha()
_UP_ARROW = pygame.image.load(
    "./assets/img/up_arrow.png").convert_alpha()
_DOWN_ARROW = pygame.image.load(
    "./assets/img/down_arrow.png").convert_alpha()

_ACTIVATED_LEFT_ARROW = pygame.image.load(
    "./assets/img/activated_left_arrow.png").convert_alpha()

_ACTIVATED_RIGHT_ARROW = pygame.image.load(
    "./assets/img/activated_right_arrow.png").convert_alpha()

_ACTIVATED_UP_ARROW = pygame.image.load(
    "./assets/img/activated_up_arrow.png").convert_alpha()

_ACTIVATED_DOWN_ARROW = pygame.image.load(
    "./assets/img/activated_down_arrow.png").convert_alpha()



class Font:
    TITLE_FONT = pygame.font.Font(
        './assets/font/FridayFunkin-Regular.ttf', 100)
    TITLE_FONT_2 = pygame.font.Font(
        './assets/font/FridayFunkin-Regular.ttf', 75)
    WEEK_FONT = pygame.font.Font('./assets/font/FridayFunkin-Regular.ttf', 50)
    SCORE_FONT = pygame.font.Font('./assets/font/Gtoles.ttf', 300)
    MENU_SCORE = pygame.font.Font('./assets/font/vcr_osd.ttf', 20)


class Gallery:
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

    ENTITY_IDLE = './assets/img/idle.mp4'
    ENTITY_LEFT = './assets/img/left.mp4'
    ENTITY_RIGHT = './assets/img/right.mp4'
    ENTITY_UP = './assets/img/up.mp4'
    ENTITY_DOWN = './assets/img/down.mp4'

    LOGO = pygame.image.load("./assets/img/logo.jpg").convert()

    BUTTON_DEACTIVATED_IMAGES = (pygame.transform.rotozoom(pygame.image.load("./assets/img/play_1.jpg").convert(
    ), 0, 0.6), pygame.transform.rotozoom(pygame.image.load("./assets/img/play_2.jpg").convert(), 0, 0.6))
    BUTTON_ON_HOVER_IMAGES = (pygame.transform.rotozoom(pygame.image.load("./assets/img/play_3.png").convert_alpha(
    ), 0, 0.6), pygame.transform.rotozoom(pygame.image.load("./assets/img/play_4.png").convert_alpha(), 0, 0.6))
    BUTTON_ACTIVATED_IMAGES = (pygame.transform.rotozoom(pygame.image.load("./assets/img/play_1.jpg").convert_alpha(
    ), 0, 0.6), pygame.transform.rotozoom(pygame.image.load("./assets/img/play_3.png").convert_alpha(), 0, 0.6))

    POINTER = (pygame.transform.rotozoom(pygame.image.load("./assets/img/pointer_1.png").convert_alpha(), 0, 0.2),
               pygame.transform.rotozoom(pygame.image.load("./assets/img/pointer_2.png").convert_alpha(), 0, 0.2))

class Data:
    descriptions = file_loader.description_parser(file_loader.file_parser())
    
class Audio:
    FREAKY_MENU = pygame.mixer.Sound('./assets/audio/freaky_menu.ogg')
    CONFIRM_MENU = pygame.mixer.Sound('./assets/audio/confirm_menu.ogg')
    SCROLL_MENU = pygame.mixer.Sound('./assets/audio/scroll_menu.ogg')

    SOUTH_INSTRUMENT = pygame.mixer.Sound(
        "./assets/audio/south_instrument.ogg")
    SOUTH_VOCAL = pygame.mixer.Sound('./assets/audio/south_vocal.ogg')

    TUTORIAL = pygame.mixer.Sound('./assets/audio/tutorial.ogg')

    VOCAL_VOLUME = 1