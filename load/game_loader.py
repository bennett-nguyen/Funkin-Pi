"""
Load all of the resources for this game and initialize the display surface
"""
import pygame
from pygame.locals import *
from dataclasses import dataclass
import load.file_loader as file_loader
import general_component.constant as const

flags = FULLSCREEN | DOUBLEBUF

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])
pygame.display.set_caption("Funky Friday at Home")

@dataclass
class _SharedData:
    """
    Defines the data that will be shared across all components
    """
    dt: float
    events: pygame.event

shared_data = _SharedData(None, None)


class DisplaySurf:
    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))

# Video animation must be 600x690px


# Images
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

_SICK = pygame.image.load("./assets/img/borrowed/sick.png").convert_alpha()
_GOOD = pygame.image.load("./assets/img/borrowed/good.png").convert_alpha()
_BAD = pygame.image.load("./assets/img/borrowed/bad.png").convert_alpha()
class _Font:
    # TITLE_SIZE = 100
    # TITLE_SIZE_2 = 75
    # TITLE_SIZE_3 = 50
    # MENU_SCORE = 20

    DEPRECATED_FNF_FONT = './assets/font/FridayFunkin-Regular.ttf'
    VRC_OSD = './assets/font/vcr_osd.ttf'
    PHANTOMMUFF_EMPTY = './assets/font/PhantomMuff Empty Letters.ttf'
    PHANTOMMUFF_FULL = './assets/font/PhantomMuff Full Letters.ttf'

    def __init__(self):
        self.FONT_MAP = {
            "vrc-osd": self.VRC_OSD,
            "deprecated-fnf-font": self.DEPRECATED_FNF_FONT,
            "phantommuff-empty": self.PHANTOMMUFF_EMPTY,
            "phantommuff-full": self.PHANTOMMUFF_FULL
        }

    def get_font(self, name: str, size: int):
        """
        Available fonts: 
        - vrc-osd
        - deprecated-fnf-font
        - phantommuff-empty
        - phantommuff-full
        
        Standard size:
        - title font 1: 100
        - title font 2: 75
        - title font 3: 50
        - menu score: 20
        """
        return pygame.font.Font(self.FONT_MAP[name], size)

CustomFont = _Font()

_title_font = CustomFont.get_font("phantommuff-empty", 80)
_title_font_1 = CustomFont.get_font("phantommuff-empty", const.TITLE_SIZE)

_message_1 = _title_font_1.render(" ", True, "White")
_message_1_rect = _message_1.get_rect(center = (const.MESSAGE_X, const.MESSAGE_1_Y))

_message_2 = _title_font.render("BENNETT NGUYEN'S PRESENT", True, "White")
_message_2_rect = _message_2.get_rect(center = (const.MESSAGE_X, const.MESSAGE_2_Y))

_message_3 = _title_font_1.render(" ", True, "White")
_message_3_rect = _message_3.get_rect(center = (const.MESSAGE_X, const.MESSAGE_3_Y))



_message_4 = _title_font_1.render("MADE", True, "White")
_message_4_rect = _message_4.get_rect(center = (const.MESSAGE_X, const.MESSAGE_1_Y))

_message_5 = _title_font_1.render("WITH", True, "White")
_message_5_rect = _message_5.get_rect(center = (const.MESSAGE_X, const.MESSAGE_2_Y))

_message_6 = _title_font_1.render("PYTHON AND PYGAME", True, "White")
_message_6_rect = _message_6.get_rect(center = (const.MESSAGE_X, const.MESSAGE_3_Y))



_message_7 = _title_font_1.render("FROM THE", True, "White")
_message_7_rect = _message_7.get_rect(center = (const.MESSAGE_X, const.MESSAGE_1_Y))

_message_8 = _title_font_1.render("AMAZING", True, "White")
_message_8_rect = _message_8.get_rect(center = (const.MESSAGE_X, const.MESSAGE_2_Y))

_message_9 = _title_font_1.render("FRIDAY NIGHT FUNKIN'", True, "White")
_message_9_rect = _message_9.get_rect(center = (const.MESSAGE_X, const.MESSAGE_3_Y))

class Message:
    _req_message_list_1 = [
        (_message_1, _message_1_rect),
        (_message_2, _message_2_rect),
        (_message_3, _message_3_rect)
    ]
    
    _req_message_list_2 = [
        (_message_4, _message_4_rect),
        (_message_5, _message_5_rect),
        (_message_6, _message_6_rect)
    ]
    
    _req_message_list_3 = [
        (_message_7, _message_7_rect),
        (_message_8, _message_8_rect),
        (_message_9, _message_9_rect)
    ]
    
    _opt_message_list = file_loader.load_opt_message()


_scale = 2  # Increase this to get smaller arrow images
_game_message_scale = 1.5
_game_message_scale_2 = 1.7
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

    SICK = pygame.transform.scale(_SICK, (_SICK.get_width() / _game_message_scale_2, _SICK.get_height() / _game_message_scale_2))
    GOOD = pygame.transform.scale(_GOOD, (_GOOD.get_width() / _game_message_scale, _GOOD.get_height() / _game_message_scale))
    BAD =  pygame.transform.scale(_BAD, (_BAD.get_width() / _game_message_scale, _BAD.get_height() / _game_message_scale))

    LOGO = pygame.image.load("./assets/img/logo.jpg").convert()
    PAUSED_BACKGROUND = pygame.image.load("./assets/img/paused_template.png").convert_alpha()

    PLAY_BUTTON_DEACTIVATED_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/play_1.jpg").convert(), 0, 0.6),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/play_2.jpg").convert(), 0, 0.6)
    )
    PLAY_BUTTON_ON_HOVER_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/play_3.png").convert_alpha(), 0, 0.6),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/play_4.png").convert_alpha(), 0, 0.6)
    )
    PLAY_BUTTON_ACTIVATED_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/play_1.jpg").convert(), 0, 0.6),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/play_3.png").convert_alpha(), 0, 0.6)
    )
    
    PS_BUTTON_SCALE = 0.6

    CONTINUE_BUTTON_DEACTIVATED_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/continue_1.png").convert_alpha(), 0, PS_BUTTON_SCALE),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/continue_2.png").convert_alpha(), 0, PS_BUTTON_SCALE)
    )
    CONTINUE_BUTTON_ON_HOVER_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/continue_3.png").convert_alpha(), 0, PS_BUTTON_SCALE),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/continue_4.png").convert_alpha(), 0, PS_BUTTON_SCALE)
    )

    EXIT_BUTTON_DEACTIVATED_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/exit_1.png").convert_alpha(), 0, PS_BUTTON_SCALE),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/exit_2.png").convert_alpha(), 0, PS_BUTTON_SCALE)
    )
    EXIT_BUTTON_ON_HOVER_IMAGES = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/exit_3.png").convert_alpha(), 0, PS_BUTTON_SCALE),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/exit_4.png").convert_alpha(), 0, PS_BUTTON_SCALE)
    )

    POINTER = (
        pygame.transform.rotozoom(pygame.image.load("./assets/img/pointer_1.png").convert_alpha(), 0, 0.2),
        pygame.transform.rotozoom(pygame.image.load("./assets/img/pointer_2.png").convert_alpha(), 0, 0.2)
    )
    


class Data:
    descriptions = file_loader.data_parser(file_loader.file_parser())

class Audio:
    FREAKY_MENU = pygame.mixer.Sound('./assets/audio/freaky_menu.ogg')
    CONFIRM_MENU = pygame.mixer.Sound('./assets/audio/confirm_menu.ogg')
    SCROLL_MENU = pygame.mixer.Sound('./assets/audio/scroll_menu.ogg')
    
    # INTRO_1 = pygame.mixer.Sound('./assets/audio/intro1.ogg')
    # INTRO_2 = pygame.mixer.Sound('./assets/audio/intro2.ogg')
    # INTRO_3 = pygame.mixer.Sound('./assets/audio/intro3.ogg')
    # INTRO_GO = pygame.mixer.Sound('./assets/audio/introGo.ogg')
    

    VOCAL_VOLUME = 1