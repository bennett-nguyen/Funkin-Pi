import pygame
import load.game_loader as game_loader

pygame.init()


class Scene:
    def __init__(self):
        self.redirect = None
        self.redirect_delay = 0
        self.allow_keydown = True

        self.fade_delay = 0

    def input(self):
        pass

    def redraw(self):
        pass

    def reset_attr(self):
        self.redirect = None
        self.allow_keydown = False


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
        main_game_data = getattr(self.current, 'loaded_data', None)
        self.current.reset_attr()
        self.current = self.scenes[state]
        if main_game_data is not None:
            self.current.receive_data(main_game_data)
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

        self.track_index = self.diff_index = 0
        self.current_track = self.tracks[self.track_index]

        self.avail_diff = self.current_track.available_difficulties
        self.curr_diff_text = self.current_track.difficulties[
            self.avail_diff[self.diff_index]]
        self.prev_diff = self.avail_diff[self.diff_index]
        
        self.current_score = self.current_track.score
        
        self.score_text = game_loader.Font.MENU_SCORE.render(
            f"SCORE: {self.current_score[self.prev_diff]}", True, "White")
        self.st_rect = self.score_text.get_rect(
            midleft=(75, 25))
        
        self.speed = 20
        self.jumping_speed = 30

        self.unfocus_alpha = 100

        self.current_time = self.keydown_time = 0
        self.delay_time = 250

        self.difficulty_centery = self.curr_diff_text[1].centery
        self.offset_centery = -70
        self.alpha = 50

        self.is_transitioning = self.is_moving_up = self.is_moving_down = self.jumping = self.changing_difficulty = self.on_keydown_delay = False

    def difficulty_animation(self):

        if self.changing_difficulty:
            self.curr_diff_text[1].centery += 10
            self.offset_centery += 10
            self.alpha += 36.4

        if not self.offset_centery:
            self.curr_diff_text[1].centery = self.difficulty_centery
            self.changing_difficulty = self.is_transitioning = False
            self.offset_centery = -70
            self.alpha = 50
            self.curr_diff_text[0].set_alpha(255)

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
        self.current_time = pygame.time.get_ticks()

        if self.current_time - self.keydown_time > self.delay_time:
            self.on_keydown_delay = False

        if not self.on_keydown_delay and not self.is_transitioning:
            if key[pygame.K_UP]:
                self.keydown_time = pygame.time.get_ticks()
                self.on_keydown_delay = self.is_transitioning = True
                if self.track_index >= 1:
                    self.is_moving_down = True
                    self.track_index -= 1
                else:
                    self.is_moving_up = self.jumping = True
                    self.track_index = len(self.tracks) - 1

                game_loader.Audio.SCROLL_MENU.play()

            elif key[pygame.K_DOWN]:
                self.keydown_time = pygame.time.get_ticks()
                self.on_keydown_delay = self.is_transitioning = True

                if self.track_index + 1 < len(self.tracks):
                    self.is_moving_up = True
                    self.track_index += 1
                else:
                    self.is_moving_down = self.jumping = True
                    self.track_index = 0

                game_loader.Audio.SCROLL_MENU.play()

            elif key[pygame.K_LEFT]:
                self.keydown_time = pygame.time.get_ticks()
                self.on_keydown_delay = self.is_transitioning = self.changing_difficulty = True

                if self.diff_index >= 1:
                    self.diff_index -= 1
                else:
                    self.diff_index = len(self.avail_diff)-1

                game_loader.Audio.SCROLL_MENU.play()

            elif key[pygame.K_RIGHT]:
                self.keydown_time = pygame.time.get_ticks()
                self.on_keydown_delay = self.is_transitioning = self.changing_difficulty = True

                if self.diff_index + 1 < len(self.avail_diff):
                    self.diff_index += 1
                else:
                    self.diff_index = 0

                game_loader.Audio.SCROLL_MENU.play()

            self.process_input_data()
    
    def load_track_data(self):
        return {
            "name": self.current_track.name,
            "chosen_difficulty": self.prev_diff,
            "difficulty_config": self.current_track.difficulties_config[self.prev_diff],
            "objects": self.current_track.objects[self.prev_diff]
        }

    def process_input_data(self):
        prev_avail_diffs = self.avail_diff
        prev_diff_index = prev_avail_diffs.index(
            self.prev_diff)


        self.current_track = self.tracks[self.track_index]
        self.avail_diff = self.current_track.available_difficulties


        if self.prev_diff not in self.avail_diff:
            self.diff_index = 0
            self.is_transitioning = self.changing_difficulty = True

        elif prev_diff_index != self.avail_diff.index(self.prev_diff):
            self.diff_index = self.avail_diff.index(
                self.prev_diff)


        self.curr_diff_text = self.current_track.difficulties[
            self.avail_diff[self.diff_index]]
        self.prev_diff = self.avail_diff[self.diff_index]

        self.current_score = self.current_track.score
        
        self.score_text = game_loader.Font.MENU_SCORE.render(
            f"SCORE: {self.current_score[self.prev_diff]}", True, "White")
        self.st_rect = self.score_text.get_rect(
            midleft=(75, 25))

        if self.changing_difficulty:
            self.curr_diff_text[1].centery += self.offset_centery
            self.curr_diff_text[0].set_alpha(self.alpha)

    def redraw(self):
        if self.is_transitioning:
            self.move_track()

        if self.changing_difficulty:
            self.difficulty_animation()

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

            game_loader.DisplaySurf.Screen.blit(
                self.curr_diff_text[0], self.curr_diff_text[1]
            )

            game_loader.DisplaySurf.Screen.blit(self.score_text, self.st_rect)
    def update(self):
        self.input()
        self.redraw()
