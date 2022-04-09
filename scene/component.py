import pygame
import load.game_loader as game_loader

pygame.init()


class Scene:
    def __init__(self):
        self.redirect = None
        self.redirect_delay = 0

        self.fade_delay = 0

    def input(self):
        pass

    def redraw(self):
        pass

    def reset_attr(self):
        self.redirect = None

    def set_direct(self):
        pass


class SceneSwitcher:
    def __init__(self, scenes: dict):
        self.scenes = scenes
        self.current = self.scenes["start screen"]
        self.is_transitioning = False
        self.redirect_delay = 0

        self.current_time = 0
        self.redirected_time = 0

        self.screen = pygame.Surface(
            game_loader.DisplaySurf.Screen.get_size())
        self.screen.fill((0, 0, 0))

        self.alpha = 0
        self.fade_delay = 0
        self.fade_state = "OUT"

    def change_scene(self):
        state = self.current.redirect
        self.current.reset_attr()
        self.current = self.scenes[state]
        self.reset_attr()

    def fade(self):
        if self.fade_state == "OUT":
            self.alpha += 4
            self.screen.set_alpha(self.alpha)
            game_loader.DisplaySurf.Screen.blit(self.screen, (0, 0))

            if self.alpha >= 255:
                self.fade_state = "IN"

        elif self.fade_state == "IN":
            self.alpha -= 4
            self.screen.set_alpha(self.alpha)
            game_loader.DisplaySurf.Screen.blit(self.screen, (0, 0))

            if self.alpha <= 0:
                self.fade_state = "OUT"
                self.alpha = 0
                self.is_transitioning = False
                self.fade_delay = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()

        if not self.is_transitioning:
            self.current.input()
        self.current.redraw()

        if self.current.redirect is not None:
            if not self.redirected_time:
                self.redirected_time = pygame.time.get_ticks()
                self.redirect_delay = self.current.redirect_delay
                self.fade_delay = self.current.fade_delay
                self.is_transitioning = True

            if self.current_time - self.redirected_time > self.redirect_delay:
                self.change_scene()

        if (
            self.is_transitioning
            and self.current_time - self.redirected_time > self.fade_delay
        ):
            self.fade()

    def reset_attr(self):
        self.redirect_delay = self.redirected_time = 0


class MenuLogic:
    def __init__(self, tracks):
        self.tracks = tracks
        self.centery = self.tracks[0].display_name_rect.centery
        
        self.track_index = 0
        self.current_track = self.tracks[self.track_index]

        self.speed = 20
        self.jumping_speed = 30
        
        self.unfocus_alpha = 100

        self.is_transitioning = self.is_moving_up = self.is_moving_down = self.jumping = False

    def move_track(self):
        if self.is_transitioning:
            for track in self.tracks:
                if self.is_moving_up:
                    track.display_name_rect.centery -= self.jumping_speed if self.jumping else self.speed
                elif self.is_moving_down:
                    track.display_name_rect.centery += self.jumping_speed if self.jumping else self.speed

            if self.current_track.display_name_rect.centery == self.centery:
                self.is_moving_down = self.is_moving_up = self.is_transitioning = self.jumping = False

    def input(self):
        key = pygame.key.get_pressed()

        if not self.is_transitioning:
            if key[pygame.K_UP]:

                self.is_transitioning = True

                if self.track_index >= 1:
                    self.is_moving_down = True
                    self.track_index -= 1
                else:
                    self.is_moving_up = True
                    self.jumping = True
                    self.track_index = len(self.tracks) - 1

                game_loader.Audio.SCROLL_MENU.play()

            elif key[pygame.K_DOWN]:
                
                self.is_transitioning = True

                if self.track_index + 1 < len(self.tracks):
                    self.is_moving_up = True
                    self.track_index += 1
                else:
                    self.is_moving_down = True
                    self.jumping = True
                    self.track_index = 0

                game_loader.Audio.SCROLL_MENU.play()

            self.current_track = self.tracks[self.track_index]

    def redraw(self):
        if self.is_transitioning:
            self.move_track()

        for track in self.tracks:
            if track.display_name_rect.bottom < 250 or track.display_name_rect.top > game_loader.DisplaySurf.HEIGHT:
                continue

            if track == self.current_track:
                track.display_name.set_alpha(255)
            else:
                track.display_name.set_alpha(self.unfocus_alpha)

            
            # only render text that is below the yellow rectangle or below the screen height
            game_loader.DisplaySurf.Screen.blit(
                track.display_name, track.display_name_rect)

    def update(self):
        self.input()
        self.redraw()
