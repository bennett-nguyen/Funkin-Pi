import pygame as pg
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const

pg.init()

class MenuLogic:
    def __init__(self, tracks):
        menu_score_font = assets.CustomFont.get_font("vrc-osd", const.MENU_SCORE)

        self.tracks = tracks
        self.centery = self.tracks[0].display_name_rect.centery

        self.track_index = self.diff_index = 0
        self.current_track = self.tracks[self.track_index]

        self.avail_diff = self.current_track.available_difficulties
        self.curr_diff_text = self.current_track.difficulties[self.avail_diff[self.diff_index]]
        self.prev_diff = self.avail_diff[self.diff_index]

        self.current_score = self.current_track.score

        self.score_text = menu_score_font.render(f"SCORE: {self.current_score[self.prev_diff]}", True, "White")
        self.st_rect = self.score_text.get_rect(midleft=(75, 25))

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
        key = pg.key.get_pressed()
        self.current_time = pg.time.get_ticks()

        if self.current_time - self.keydown_time > self.delay_time:
            self.on_keydown_delay = False

        if all(
            (
                not (self.on_keydown_delay or self.is_transitioning),
                any((key[pg.K_UP], key[pg.K_DOWN],
                    key[pg.K_LEFT], key[pg.K_RIGHT]))
            )
        ):
            self.keydown_time = pg.time.get_ticks()
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
            
            "hb_enemy_rgb": self.current_track.hb_enemy_rgb,
            "hb_player_rgb": self.current_track.hb_player_rgb
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

        menu_score_font = assets.CustomFont.get_font("vrc-osd", const.MENU_SCORE)
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
            if track.display_name_rect.bottom < 250 or track.display_name_rect.top > const.HEIGHT:
                continue

            if track == self.current_track:
                track.display_name.set_alpha(255)
            else:
                track.display_name.set_alpha(self.unfocus_alpha)

            # only render text that is below the yellow rectangle or below the screen height
            ds.screen.blit(track.display_name, track.display_name_rect)
            ds.screen.blit(self.curr_diff_text[0], self.curr_diff_text[1])
            ds.screen.blit(self.score_text, self.st_rect)

    def key_up_n_down(self, key):
        track_len = len(self.tracks)

        if key[pg.K_UP]:

            if min(0, self.track_index - 1):
                self.is_moving_up = self.jumping = track_len > 1
                self.track_index = track_len - 1 if track_len > 1 else self.track_index
            else:
                self.is_moving_down = True
                self.track_index -= 1

            assets.Audio.SCROLL_MENU.play()

        elif key[pg.K_DOWN]:

            if self.track_index + 1 < track_len:
                self.is_moving_up = True
                self.track_index += 1
            else:
                self.is_moving_down = self.jumping = track_len > 1
                self.track_index = 0 if track_len > 1 else self.track_index

            assets.Audio.SCROLL_MENU.play()

    def key_left_n_right(self, key):
        avail_diff_len = len(self.avail_diff)

        if key[pg.K_LEFT]:
            self.changing_difficulty = True

            if self.diff_index >= 1:
                self.diff_index -= 1
            else:
                self.diff_index = avail_diff_len - 1

            assets.Audio.SCROLL_MENU.play()

        elif key[pg.K_RIGHT]:
            self.changing_difficulty = True

            if self.diff_index + 1 < avail_diff_len:
                self.diff_index += 1
            else:
                self.diff_index = 0

            assets.Audio.SCROLL_MENU.play()