import pygame
import game_loader
import cv2
from itertools import cycle

pygame.init()

image_loader = game_loader.Gallery

# -------- Components for the main game ----------
class Surface:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int] = None):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) if color is None else pygame.Surface((width, height))
        if color is not None:self.surface.fill(color)
        self.rect = self.surface.get_rect(center=(x, y))


class TransparentSurf(Surface):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH/2/1.3, 70)

        self.left_arrow = image_loader.LEFT_ARROW
        self.up_arrow = image_loader.UP_ARROW
        self.down_arrow = image_loader.DOWN_ARROW
        self.right_arrow = image_loader.RIGHT_ARROW

        self.left_arrow_rect = self.left_arrow.get_rect(
            midleft=(self.rect.midleft[0] + 25, self.rect.midleft[1]))
        self.down_arrow_rect = self.down_arrow.get_rect(
            midleft=(self.rect.midleft[0] + 135, self.rect.midleft[1]))
        self.up_arrow_rect = self.up_arrow.get_rect(
            midright=(self.rect.midright[0] - 135, self.rect.midright[1]))
        self.right_arrow_rect = self.right_arrow.get_rect(
            midright=(self.rect.midright[0] - 25, self.rect.midright[1]))

    def draw_arrow(self):
        game_loader.DisplaySurf.Screen.blit(
            self.left_arrow, self.left_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(
            self.up_arrow, self.up_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(
            self.down_arrow, self.down_arrow_rect)
        game_loader.DisplaySurf.Screen.blit(
            self.right_arrow, self.right_arrow_rect)

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


class FlyingSurf(Surface):
    VEL = 7

    def __init__(self, x: int, y: int, arrow: game_loader.Gallery) -> None:
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH/2/1.3, 70)

        self.arrow = arrow

        match self.arrow:
            case game_loader.Gallery.ACTIVATED_LEFT_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midleft=(self.rect.midleft[0] + 25, self.rect.midleft[1]))
                self.key = pygame.K_LEFT

            case game_loader.Gallery.ACTIVATED_DOWN_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midleft=(self.rect.midleft[0] + 135, self.rect.midleft[1]))
                self.key = pygame.K_DOWN

            case game_loader.Gallery.ACTIVATED_UP_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midright=(self.rect.midright[0] - 135, self.rect.midleft[1]))
                self.key = pygame.K_UP

            case game_loader.Gallery.ACTIVATED_RIGHT_ARROW:
                self.arrow_rect = self.arrow.get_rect(
                    midright=(self.rect.midright[0] - 25, self.rect.midright[1]))
                self.key = pygame.K_RIGHT

    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        game_loader.DisplaySurf.Screen.blit(self.arrow, self.arrow_rect)

    def move(self):
        self.rect.y -= self.VEL
        self.arrow_rect.y -= self.VEL

    def collide(self, object):
        # range from object.rect.center[1] + range --> object.rect.center[1] - range
        # the shorter the range, the harder you'll get a sick move
        range = 8
        target = self.rect
        lowest_center_range = object.rect.center[1] - range
        highest_center_range = object.rect.center[1] + range

        if target.center[1] >= lowest_center_range and target.center[1] <= highest_center_range and target.colliderect(object.rect):
            print('sick')
            return True

        elif target.colliderect(object.rect):
            print('good')
            return True

    # this method is only used for the enemy!
    def collide_for_enemy(self, object):
        return self.rect.center[1] <= object.rect.center[1] and self.rect.colliderect(object)


class Entity(Surface):
    def __init__(self, x: int, y: int) -> None:
        
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH /
                         2, game_loader.DisplaySurf.HEIGHT)

        self.state = cv2.VideoCapture(image_loader.ENTITY_IDLE)

    def animation_is_playable(self):
        success, _ = self.state.read()
        return success

    def change_animation(self, animation_path):
        self.state = cv2.VideoCapture(animation_path)

    def load_animation(self):
        success, frame = self.state.read()

        if not success:
            return

        self.animation_surf = pygame.image.frombuffer(
            frame.tobytes(), frame.shape[1::-1], "BGR")
        self.animation_rect = self.animation_surf.get_rect(
            center=self.rect.center)

    def draw_self(self):
        game_loader.DisplaySurf.Screen.blit(self.surface, self.rect)
        game_loader.DisplaySurf.Screen.blit(
            self.animation_surf, self.animation_rect)
# ----------------------------------------------------



# --------Components for the start screen --------
class ImageAnimation:
    def __init__(self, images: tuple, x: int, y: int, speed: float):
        self.images = images
        self.index = 0
        self.speed = speed  # 0 -> 1 high speed == fast animation

        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(center=(x, y))

    def toggle_animation(self):
        self.index += self.speed
        if self.index >= len(self.images):
            self.index = 0
        self.surf = self.images[int(self.index)]

        game_loader.DisplaySurf.Screen.blit(self.surf, self.rect)


# still under construction
class Track:
    def __init__(self, name: str, difficulties: list[str], score: dict):
        self.display_name = game_loader.Font.TITLE_FONT_2.render(
            name.upper(), True, (255, 255, 255))

        self.difficulties = [
            game_loader.Font.TITLE_FONT_2.render(difficulty.upper(), True, (255, 255, 255))
            for difficulty in difficulties
            if difficulty.lower() in ["easy", "normal"]
        ]
        self.score = score
        
        self.alpha = 255
        self.display_name.set_alpha(self.alpha)
        
    def move_up(self):
        self.display_name_rect.y -= 100
    
    def move_down(self):
        self.display_name_rect.y += 100
        
    def init_rect_coordinates(self, x, y):
        self.display_name_rect = self.display_name.get_rect(center = (x, y))

class TrackChooser(Surface):
    def __init__(self, x: int, y: int, width, height, tracks: list[Track]):
        pass


def file_parser() -> list[dict]:
    import json
    import os
    files = []

    try:
        for entry in os.listdir("./mapping/header"):
            if not entry.endswith(".json"):
                continue

            with open(f"./mapping/header/{entry}", "r") as f:
                file = json.load(f)
                files.append(file)
    except Exception as e:
        print("an exception occurred during runtime:")
        print(e)
        raise Exception('exited due to errors')

    return files


def description_parser(files: list[dict]) -> list[Track]:
    return [
        Track(file["description"]["name"], file["description"]["difficulties"], file["description"]["score"])
        for file in files
        if "description" in file
    ]
# ------------------------------------------------


# -------- Components for screen transitioning ---
class Scene:
    def __init__(self):
        pass
        
    def update(self):
        self.input()
        self.redraw()
    
    def input(self):
        pass
    
    def redraw(self):
        pass
    
    def reset_attr(self):
        pass
    
    def set_direct(self):
        pass


class SceneSwitcher:
    def __init__(self, scenes: dict):
        self.scenes = scenes
        
    def next(self):
        pass
    
    def redraw(self):
        pass
    
    def update(self):
        pass


class StartScreen(Scene):
    def __init__(self):
        self.sound_1_effect_played = self.sound_2_effect_played = self.button_pressed = False

        self.deactivated_button = ImageAnimation(
            game_loader.Gallery.BUTTON_DEACTIVATED_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.1)
        self.on_hover_button = ImageAnimation(
            game_loader.Gallery.BUTTON_ON_HOVER_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.1)
        self.activated_button = ImageAnimation(
            game_loader.Gallery.BUTTON_ACTIVATED_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.15)
        self.button_hit_box = Surface(
            game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 250, 120)
        
        self.redirect = None
        self.redirect_delay = 2000
        
        self.button_pressed_time = 0
        self.current_time = 0

    def redraw(self):
        game_loader.DisplaySurf.Screen.blit(game_loader.Gallery.LOGO, game_loader.Gallery.LOGO.get_rect(
            center=(game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2)))

        if self.button_pressed:
            self.activated_button.toggle_animation()

        if not self.button_pressed:
            if self.button_hit_box.rect.collidepoint(pygame.mouse.get_pos()):
                self.on_hover_button.toggle_animation()

                if not self.sound_2_effect_played:
                    game_loader.Audio.SCROLL_MENU.play()
                    self.sound_2_effect_played = True
            else:
                self.deactivated_button.toggle_animation()
                self.sound_2_effect_played = False
        
        self.current_time = pygame.time.get_ticks()
                
    def set_direct(self):
        if self.button_pressed_time and self.current_time - self.button_pressed_time > self.redirect_delay:
            self.redirect = "menu screen"

    def input(self):
        if (
            pygame.mouse.get_pressed()[0]
            and self.button_hit_box.rect.collidepoint(pygame.mouse.get_pos())
            and not self.button_pressed_time
        ) or (pygame.key.get_pressed()[pygame.K_RETURN]):
            self.button_pressed = True
            self.button_pressed_time = pygame.time.get_ticks()
                
        if self.button_pressed and not self.sound_1_effect_played:
            game_loader.Audio.CONFIRM_MENU.play()
            self.sound_1_effect_played = True

    def reset_attr(self):
        self.sound_1_effect_played = self.sound_2_effect_played = self.button_pressed = False


class MenuScreen(Scene):
    def __init__(self):
        self.week_score = 0
        
        self.top_rectangle = Surface(game_loader.DisplaySurf.WIDTH/2, 150, game_loader.DisplaySurf.WIDTH - 150, 200, (249, 209, 81))
        self.choose_your_track = game_loader.Font.TITLE_FONT_2.render("CHOOSE YOUR TRACK", True, "Black")
        self.cyt_rect = self.choose_your_track.get_rect(center = self.top_rectangle.rect.center)
        self.score_text = game_loader.Font.MENU_SCORE.render(f"SCORE: {self.week_score}", True, "White")
        self.st_rect = self.score_text.get_rect(midleft = (self.top_rectangle.rect.midleft[0], 25))


        self.some_rectangle = Surface(game_loader.DisplaySurf.WIDTH/2, 470, 270, 300)
        self.pointer = ImageAnimation(game_loader.Gallery.POINTER, self.some_rectangle.rect.centerx + 250, self.some_rectangle.rect.centery, 0.1)
        self.tracks = description_parser(file_parser())
    
    def draw_tracks(self):
        distance = 0
    
        for track in self.tracks:
            track.init_rect_coordinates(self.some_rectangle.rect.centerx, self.some_rectangle.rect.centery + distance)
            game_loader.DisplaySurf.Screen.blit(track.display_name, track.display_name_rect)
            distance += 100
    
    def redraw(self):
        game_loader.DisplaySurf.Screen.blit(self.top_rectangle.surface, self.top_rectangle.rect)
        game_loader.DisplaySurf.Screen.blit(self.choose_your_track, self.cyt_rect)
        game_loader.DisplaySurf.Screen.blit(self.score_text, self.st_rect)
        
        self.pointer.toggle_animation()
        
        self.draw_tracks()
# ------------------------------------------------