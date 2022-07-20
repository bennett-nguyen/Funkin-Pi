import pygame
import source.load.constant as const
import inspect
from dataclasses import dataclass

pygame.init()

# Video animation must be 600x690px
# 976x1081px

@dataclass(frozen=True, init=True, eq=False, unsafe_hash=False)
class __Font:
    FONT_MAP = {
        "vrc-osd": './assets/font/vcr_osd.ttf',
        "deprecated-fnf-font": './assets/font/FridayFunkin-Regular.ttf',
        "phantommuff-empty": './assets/font/PhantomMuff Empty Letters.ttf',
        "phantommuff-full": './assets/font/PhantomMuff Full Letters.ttf'
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

CustomFont = __Font()

def _generate_message(message_list, font):
    result = []
    for index, element in enumerate(message_list):
        message = font.render(element, True, "White")
        rect = message.get_rect(center = (const.MESSAGE_X, getattr(const, f"MESSAGE_{index+1}_Y")))

        result.append((message, rect))

    return result

def _load_opt_message():
    from secrets import choice
    from json import load

    message_init_map = {
        "init_message": lambda text: CustomFont.get_font(name="phantommuff-empty", size=const.TITLE_SIZE).render(text, True, "White"),
        "get_rect": lambda surf, x, y: surf.get_rect(center = (x, y))
    }

    with open("./assets/optional-message.json", "r") as f:
        file = load(f)
        message = choice(file["random"])
        result = []
        for i in range(1, 4):
            message_surf = message_init_map["init_message"](message[f"message_{i}"].upper())
            message_rect = message_init_map["get_rect"](message_surf, const.MESSAGE_X, getattr(const, f"MESSAGE_{i}_Y"))
            result.append((message_surf, message_rect))

        return result
    

@dataclass(frozen=True, init=False, eq=False, unsafe_hash=False)
class Message:
    opt_message_list = _load_opt_message()
    req_message_list_1 = _generate_message([" ", "BENNETT NGUYEN'S PRESENT", " "], CustomFont.get_font("phantommuff-empty", 80))
    req_message_list_2 = _generate_message(["MADE", "WITH", "PYTHON AND PYGAME"], CustomFont.get_font("phantommuff-empty", const.TITLE_SIZE))
    req_message_list_3 = _generate_message(["FROM THE", "AMAZING", "FRIDAY NIGHT FUNKIN'"], CustomFont.get_font("phantommuff-empty", const.TITLE_SIZE))

_scale = 2  # Increase this to get smaller arrow images
_game_message_scale = 1.5
_game_message_scale_2 = 1.7

# Images
_LEFT_ARROW = pygame.image.load("./assets/img/left_arrow.png").convert_alpha()
_RIGHT_ARROW = pygame.image.load("./assets/img/right_arrow.png").convert_alpha()
_UP_ARROW = pygame.image.load("./assets/img/up_arrow.png").convert_alpha()
_DOWN_ARROW = pygame.image.load("./assets/img/down_arrow.png").convert_alpha()

_ACTIVATED_LEFT_ARROW = pygame.image.load("./assets/img/activated_left_arrow.png").convert_alpha()
_ACTIVATED_RIGHT_ARROW = pygame.image.load("./assets/img/activated_right_arrow.png").convert_alpha()
_ACTIVATED_UP_ARROW = pygame.image.load("./assets/img/activated_up_arrow.png").convert_alpha()
_ACTIVATED_DOWN_ARROW = pygame.image.load("./assets/img/activated_down_arrow.png").convert_alpha()

_SICK = pygame.image.load("./assets/img/borrowed/sick.png").convert_alpha()
_GOOD = pygame.image.load("./assets/img/borrowed/good.png").convert_alpha()
_BAD = pygame.image.load("./assets/img/borrowed/bad.png").convert_alpha()

_ONE = pygame.image.load("./assets/img/1.png").convert_alpha()
_TWO = pygame.image.load("./assets/img/2.png").convert_alpha()
_THREE = pygame.image.load("./assets/img/3.png").convert_alpha()
_GO = pygame.image.load("./assets/img/go.png").convert_alpha()

_HEALTHBAR = pygame.image.load('./assets/img/healthbar.png').convert_alpha()

@dataclass(frozen=True, init=False, eq=False, unsafe_hash=False)
class Gallery:
    LEFT_ARROW = pygame.transform.scale(_LEFT_ARROW, (_LEFT_ARROW.get_width() / _scale, _LEFT_ARROW.get_height() / _scale))
    RIGHT_ARROW = pygame.transform.scale(_RIGHT_ARROW, (_RIGHT_ARROW.get_width() / _scale, _RIGHT_ARROW.get_height() / _scale))
    UP_ARROW = pygame.transform.scale(_UP_ARROW, (_UP_ARROW.get_width() / _scale, _UP_ARROW.get_height() / _scale))
    DOWN_ARROW = pygame.transform.scale(_DOWN_ARROW, (_DOWN_ARROW.get_width() / _scale, _DOWN_ARROW.get_height() / _scale))

    ACTIVATED_LEFT_ARROW = pygame.transform.scale(_ACTIVATED_LEFT_ARROW, (_ACTIVATED_LEFT_ARROW.get_width() / _scale, _ACTIVATED_LEFT_ARROW.get_height() / _scale))
    ACTIVATED_RIGHT_ARROW = pygame.transform.scale(_ACTIVATED_RIGHT_ARROW, (_ACTIVATED_RIGHT_ARROW.get_width() / _scale, _ACTIVATED_RIGHT_ARROW.get_height() / _scale))
    ACTIVATED_UP_ARROW = pygame.transform.scale(_ACTIVATED_UP_ARROW, (_ACTIVATED_UP_ARROW.get_width() / _scale, _ACTIVATED_UP_ARROW.get_height() / _scale))
    ACTIVATED_DOWN_ARROW = pygame.transform.scale(_ACTIVATED_DOWN_ARROW, (_ACTIVATED_DOWN_ARROW.get_width() / _scale, _ACTIVATED_DOWN_ARROW.get_height() / _scale))

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

    ONE = _ONE
    TWO = _TWO
    THREE = _THREE
    GO = _GO

    HEALTH_BAR_TEMPLATE = pygame.transform.rotozoom(_HEALTHBAR, 0, const.HEALTHBAR_SCALE)

@dataclass(frozen=True, init=False, eq=False, unsafe_hash=False)
class Audio:
    FREAKY_MENU = './assets/audio/freaky_menu.ogg'
    CONFIRM_MENU = pygame.mixer.Sound('./assets/audio/confirm_menu.ogg')
    SCROLL_MENU = pygame.mixer.Sound('./assets/audio/scroll_menu.ogg')

    INTRO_1 = pygame.mixer.Sound('./assets/audio/intro1.ogg')
    INTRO_2 = pygame.mixer.Sound('./assets/audio/intro2.ogg')
    INTRO_3 = pygame.mixer.Sound('./assets/audio/intro3.ogg')
    INTRO_GO = pygame.mixer.Sound('./assets/audio/introGo.ogg')

    MISS_NOTE_SOUND = (pygame.mixer.Sound('./assets/audio/missnote1.ogg'), pygame.mixer.Sound('./assets/audio/missnote2.ogg'), pygame.mixer.Sound('./assets/audio/missnote3.ogg'))

pygame.mixer.music.load(Audio.FREAKY_MENU)