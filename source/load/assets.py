import pygame as pg
import source.load.constant as const
from dataclasses import dataclass
from source.load.spritesheet import Spritesheet

pg.init()

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
        return pg.font.Font(self.FONT_MAP[name], size)


CustomFont = __Font()


def _generate_message(message_list, font):
    result = []
    for index, element in enumerate(message_list):
        message = font.render(element, True, "White")
        rect = message.get_rect(center=(const.MESSAGE_X, getattr(const, f"MESSAGE_{index+1}_Y")))

        result.append((message, rect))

    return result


def _load_opt_message():
    from secrets import choice
    from json import load

    message_init_map = {
        "init_message": lambda text: CustomFont.get_font(name="phantommuff-empty", size=const.TITLE_SIZE).render(text, True, "White"),
        "get_rect": lambda surf, x, y: surf.get_rect(center=(x, y))
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


# Images
play_button_ss = Spritesheet('./assets/img/spritesheets/play/play.png')
continue_button_ss = Spritesheet('assets/img/spritesheets/continue/continue.png')
exit_button_ss = Spritesheet('./assets/img/spritesheets/exit/exit.png')
pointer_ss = Spritesheet('./assets/img/spritesheets/pointer/pointer.png')
intro_ss = Spritesheet('./assets/img/spritesheets/intro/intro.png')
arrows_ss = Spritesheet('./assets/img/spritesheets/arrows/arrows.png')
messages_ss = Spritesheet('./assets/img/borrowed/messages/messages.png')

_HEALTHBAR = pg.image.load('./assets/img/healthbar.png').convert_alpha()

@dataclass(frozen=True, init=False, eq=False, unsafe_hash=False)
class Gallery:
    LEFT_ARROW = arrows_ss.parse_sprite('left_arrow.png')
    RIGHT_ARROW = arrows_ss.parse_sprite('right_arrow.png')
    UP_ARROW = arrows_ss.parse_sprite('up_arrow.png')
    DOWN_ARROW = arrows_ss.parse_sprite('down_arrow.png')

    ACTIVATED_LEFT_ARROW = arrows_ss.parse_sprite('activated_left_arrow.png')
    ACTIVATED_RIGHT_ARROW = arrows_ss.parse_sprite('activated_right_arrow.png')
    ACTIVATED_UP_ARROW = arrows_ss.parse_sprite('activated_up_arrow.png')
    ACTIVATED_DOWN_ARROW = arrows_ss.parse_sprite('activated_down_arrow.png')

    SICK = messages_ss.parse_sprite('sick.png', scale=0.59)
    GOOD = messages_ss.parse_sprite('good.png')
    BAD = messages_ss.parse_sprite('bad.png')

    LOGO = pg.image.load("./assets/img/logo.jpg").convert()
    PAUSED_BACKGROUND = pg.image.load("./assets/img/paused_template.png").convert_alpha()

    PLAY_BUTTON_DEACTIVATED_IMAGES = (
        play_button_ss.parse_sprite("play_1.jpg"),
        play_button_ss.parse_sprite("play_2.jpg")
    )
    PLAY_BUTTON_ON_HOVER_IMAGES = (
        play_button_ss.parse_sprite("play_3.png"),
        play_button_ss.parse_sprite("play_4.png")
    )
    PLAY_BUTTON_ACTIVATED_IMAGES = (
        play_button_ss.parse_sprite("play_1.jpg"),
        play_button_ss.parse_sprite("play_3.png")
    )

    CONTINUE_BUTTON_DEACTIVATED_IMAGES = (
        continue_button_ss.parse_sprite('continue_1.png'),
        (continue_button_ss.parse_sprite('continue_2.png'))
    )
    CONTINUE_BUTTON_ON_HOVER_IMAGES = (
        continue_button_ss.parse_sprite('continue_3.png'),
        continue_button_ss.parse_sprite('continue_4.png')
    )

    EXIT_BUTTON_DEACTIVATED_IMAGES = (
        exit_button_ss.parse_sprite('exit_1.png'),
        exit_button_ss.parse_sprite('exit_2.png')
    )
    EXIT_BUTTON_ON_HOVER_IMAGES = (
        exit_button_ss.parse_sprite('exit_3.png'),
        exit_button_ss.parse_sprite('exit_4.png')
    )

    POINTER = (
        pointer_ss.parse_sprite('pointer_1.png'),
        pointer_ss.parse_sprite('pointer_2.png')
    )

    ONE = intro_ss.parse_sprite('1.png')
    TWO = intro_ss.parse_sprite('2.png')
    THREE = intro_ss.parse_sprite('3.png')
    GO = intro_ss.parse_sprite('go.png')

    HEALTH_BAR_TEMPLATE = pg.transform.rotozoom(_HEALTHBAR, 0, const.HEALTHBAR_SCALE)


@dataclass(frozen=True, init=False, eq=False, unsafe_hash=False)
class Audio:
    FREAKY_MENU = './assets/audio/freaky_menu.ogg'
    CONFIRM_MENU = pg.mixer.Sound('./assets/audio/confirm_menu.ogg')
    SCROLL_MENU = pg.mixer.Sound('./assets/audio/scroll_menu.ogg')

    INTRO_1 = pg.mixer.Sound('./assets/audio/intro1.ogg')
    INTRO_2 = pg.mixer.Sound('./assets/audio/intro2.ogg')
    INTRO_3 = pg.mixer.Sound('./assets/audio/intro3.ogg')
    INTRO_GO = pg.mixer.Sound('./assets/audio/introGo.ogg')

    MISS_NOTE_SOUND = (pg.mixer.Sound('./assets/audio/missnote1.ogg'), pg.mixer.Sound('./assets/audio/missnote2.ogg'), pg.mixer.Sound('./assets/audio/missnote3.ogg'))


pg.mixer.music.load(Audio.FREAKY_MENU)