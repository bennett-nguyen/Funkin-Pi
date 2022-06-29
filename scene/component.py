import pygame
import load.game_loader as game_loader
import general_component.component as gcom

pygame.init()


class Scene:
    def __init__(self):
        self.redirect = None
        self.redirect_delay = 0
        self.deactivate_fade = False
        self.allow_keydown = True
        self.fade_delay = 0

    def input(self):
        """
        Defines inputs taken from the player
        """
        pass

    def redraw(self):
        """
        Defines what to redraw onto the screen each iteration
        """
        pass

    def pre_event(self):
        """
        Defines what to do before other events occur (input, redraw)
        """
        pass

    def end_pre_event(self):
        """
        Defines the condition to end pre_event (save extra running time)
        """
        return True

    def reset_attr(self):
        """
        Defines what to reset when a scene finishes work
        """
        self.redirect = None
        self.allow_keydown = False


class SceneSwitcher:
    def __init__(self, scenes: dict, start: str):
        self.scenes = scenes
        self.current = self.scenes[start]
        self.is_transitioning = False
        self.redirect_delay = 0
        self.deactivate_fade = False

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
                self.fade_delay = 0
                self.is_transitioning = False

    def update(self):
        self.current_time = pygame.time.get_ticks()

        if not self.current.end_pre_event():
            self.current.pre_event()
        
        if not self.is_transitioning:
            self.current.input()
        self.current.redraw()

        if self.current.redirect is not None:
            if not self.redirected_time:
                self.redirected_time = pygame.time.get_ticks()
                self.redirect_delay = self.current.redirect_delay
                self.deactivate_fade = self.current.deactivate_fade
                
                if not self.deactivate_fade:
                    self.fade_delay = self.current.fade_delay
                    self.is_transitioning = True

            if self.current_time - self.redirected_time > self.redirect_delay:
                self.change_scene()

        if (
            self.is_transitioning and not self.deactivate_fade
            and self.current_time - self.redirected_time > self.fade_delay
        ):
            self.fade()

    def reset_attr(self):
        self.redirect_delay = self.redirected_time = 0
        self.deactivate_fade = False


class MenuLogic:
    def __init__(self, tracks):
        menu_score_font = game_loader.CustomFont.get_font("vrc-osd", 20)

        self.tracks = tracks
        self.centery = self.tracks[0].display_name_rect.centery

        self.track_index = self.diff_index = 0
        self.current_track = self.tracks[self.track_index]

        self.avail_diff = self.current_track.available_difficulties
        self.curr_diff_text = self.current_track.difficulties[
            self.avail_diff[self.diff_index]]
        self.prev_diff = self.avail_diff[self.diff_index]

        self.current_score = self.current_track.score

        self.score_text = menu_score_font.render(
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

        if all(
            (
                not (self.on_keydown_delay or self.is_transitioning),
                any((key[pygame.K_UP], key[pygame.K_DOWN],
                    key[pygame.K_LEFT], key[pygame.K_RIGHT]))
            )
        ):
            self.keydown_time = pygame.time.get_ticks()
            self.on_keydown_delay = self.is_transitioning = True

            self.key_up_n_down(key)
            self.key_left_n_right(key)
            self.process_input_data()

    def load_track_data(self):
        return {
            "name": self.current_track.name,
            "chosen_difficulty": self.prev_diff,
            "difficulty_config": self.current_track.difficulties_config[self.prev_diff],
            "objects": self.current_track.objects[self.prev_diff],

            "instrument": self.current_track.instrument,
            "vocal": self.current_track.vocal,

            "player_entity": self.current_track.player_entity,
        }

    def process_input_data(self):
        prev_avail_diffs = self.avail_diff
        prev_diff_index = prev_avail_diffs.index(self.prev_diff)

        self.current_track = self.tracks[self.track_index]
        self.avail_diff = self.current_track.available_difficulties
        current_diff_index_of_prev = self.avail_diff.index(self.prev_diff)

        if self.prev_diff not in self.avail_diff:
            self.diff_index = 0
            self.is_transitioning = self.changing_difficulty = True

        elif prev_diff_index != current_diff_index_of_prev:
            self.diff_index = current_diff_index_of_prev


        self.curr_diff_text = self.current_track.difficulties[self.avail_diff[self.diff_index]]
        self.prev_diff = self.avail_diff[self.diff_index]

        self.current_score = self.current_track.score

        menu_score_font = game_loader.CustomFont.get_font("vrc-osd", 20)
        self.score_text = menu_score_font.render(f"SCORE: {self.current_score[self.prev_diff]}", True, "White")

        self.st_rect = self.score_text.get_rect(midleft=(75, 25))

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

    def key_up_n_down(self, key):
        track_len = len(self.tracks)

        if key[pygame.K_UP]:

            if min(0, self.track_index - 1):
                self.is_moving_up = self.jumping = track_len > 1
                self.track_index = track_len - 1 if track_len > 1 else self.track_index
            else:
                self.is_moving_down = True
                self.track_index -= 1

        elif key[pygame.K_DOWN]:

            if self.track_index + 1 < track_len:
                self.is_moving_up = True
                self.track_index += 1
            else:
                self.is_moving_down = self.jumping = track_len > 1
                self.track_index = 0 if track_len > 1 else self.track_index

        game_loader.Audio.SCROLL_MENU.play()

    def key_left_n_right(self, key):
        avail_diff_len = len(self.avail_diff)

        if key[pygame.K_LEFT]:
            self.changing_difficulty = True

            if self.diff_index >= 1:
                self.diff_index -= 1
            else:
                self.diff_index = avail_diff_len - 1

            game_loader.Audio.SCROLL_MENU.play()

        elif key[pygame.K_RIGHT]:
            self.changing_difficulty = True

            if self.diff_index + 1 < avail_diff_len:
                self.diff_index += 1
            else:
                self.diff_index = 0

            game_loader.Audio.SCROLL_MENU.play()

class PausedScreen:
    def __init__(self):
        self.background = pygame.Surface((1200, 690))
        self.background.fill("Grey")
        self.background.set_alpha(15)
        self.play_sfx_1 = False
        self.play_sfx_2 = False
        
        self.paused_background = game_loader.Gallery.PAUSED_BACKGROUND
        self.paused_background_rect = self.paused_background.get_rect(center = (game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2))

        button_speed = (0.2, 0.2, 0.2)

        self.continue_button = gcom.Button(
            (game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 30),
            (250, 120),
            game_loader.Gallery.CONTINUE_BUTTON_DEACTIVATED_IMAGES,
            game_loader.Gallery.CONTINUE_BUTTON_ON_HOVER_IMAGES,
            speed=button_speed
        )
        
        self.exit_button = gcom.Button(
            (game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 180),
            (250, 120),
            game_loader.Gallery.EXIT_BUTTON_DEACTIVATED_IMAGES,
            game_loader.Gallery.EXIT_BUTTON_ON_HOVER_IMAGES,
            speed=button_speed
        )

        self.run = False

    def _check_hover(self):
        self.continue_button.check_hover()
        self.exit_button.check_hover()

        if self.continue_button.is_on_hover:
            self.continue_button.toggle_animation(animation_type=1)
            self.exit_button.toggle_animation(animation_type=0)
            if not self.play_sfx_1:
                game_loader.Audio.SCROLL_MENU.play()
                self.play_sfx_1 = True
            return
        
        elif self.exit_button.is_on_hover:
            self.exit_button.toggle_animation(animation_type=1)
            self.continue_button.toggle_animation(animation_type=0)
            if not self.play_sfx_2:
                game_loader.Audio.SCROLL_MENU.play()
                self.play_sfx_2 = True
            return

        self.continue_button.toggle_animation(animation_type=0)
        self.exit_button.toggle_animation(animation_type=0)
        self.play_sfx_1 = self.play_sfx_2 = False


    def activate_pause_screen(self):
        while self.run:
            game_loader.DisplaySurf.Clock.tick(30)
            game_loader.DisplaySurf.Screen.blit(self.background, (0, 0))
            game_loader.DisplaySurf.Screen.blit(self.paused_background, self.paused_background_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            self._check_hover()
            self.continue_button.check_click(click_type=0)
            if self.continue_button.activated_by_click:
                self.run = False
                game_loader.DisplaySurf.Clock.tick(60)

            pygame.display.update()
