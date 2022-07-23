import pygame as pg
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
import source.load.function as fun
from sys import exit
from random import randint
from source.comp.other.button import Button

pg.init()


class PausedScreen:
    def __init__(self):
        self.background = pg.Surface((1200, 690))
        self.background.fill("Grey")
        self.background.set_alpha(15)
        self.play_sfx_1 = False
        self.play_sfx_2 = False

        self.paused_background = assets.Gallery.PAUSED_BACKGROUND
        self.paused_background_rect = self.paused_background.get_rect(center=(const.HALF_WIDTH, const.HALF_HEIGHT))

        button_speed = (0.2, 0.2, 0.2)

        self.continue_button = Button(
            (const.HALF_WIDTH, const.HALF_HEIGHT + 30),
            (250, 120),
            assets.Gallery.CONTINUE_BUTTON_DEACTIVATED_IMAGES,
            assets.Gallery.CONTINUE_BUTTON_ON_HOVER_IMAGES,
            speed=button_speed
        )

        self.exit_button = Button(
            (const.HALF_WIDTH, const.HALF_HEIGHT + 180),
            (250, 120),
            assets.Gallery.EXIT_BUTTON_DEACTIVATED_IMAGES,
            assets.Gallery.EXIT_BUTTON_ON_HOVER_IMAGES,
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
                assets.Audio.SCROLL_MENU.play()
                self.play_sfx_1 = True
            return

        elif self.exit_button.is_on_hover:
            self.exit_button.toggle_animation(animation_type=1)
            self.continue_button.toggle_animation(animation_type=0)
            if not self.play_sfx_2:
                assets.Audio.SCROLL_MENU.play()
                self.play_sfx_2 = True
            return

        self.continue_button.toggle_animation(animation_type=0)
        self.exit_button.toggle_animation(animation_type=0)
        self.play_sfx_1 = self.play_sfx_2 = False

    def activate_pause_screen(self):
        while self.run:
            ds.clock.tick(const.PAUSED_FPS)
            ds.screen.blit(self.background, (0, 0))
            ds.screen.blit(self.paused_background, self.paused_background_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            self._check_hover()
            self.continue_button.check_click(click_type=0)
            if self.continue_button.activated_by_click:
                self.run = False
                ds.clock.tick(const.FPS)

            pg.display.update()



class GameMessage:
    def __init__(self, message_code, player_arrow_set, vel, goal):
        match message_code:
            case "sick":
                self.surf = assets.Gallery.SICK.copy()
                self.rect = assets.Gallery.SICK.get_rect(center=(const.HALF_WIDTH + 10, player_arrow_set.rect.centery + 100))
            case "good":
                self.surf = assets.Gallery.GOOD.copy()
                self.rect = assets.Gallery.GOOD.get_rect(center=(const.HALF_WIDTH, player_arrow_set.rect.centery + 100))
            case "bad":
                self.surf = assets.Gallery.BAD.copy()
                self.rect = assets.Gallery.GOOD.get_rect(center=(const.HALF_WIDTH + 20, player_arrow_set.rect.centery + 100))

        self.goal_vel = goal
        self.current_vel = vel

        self.goal_alpha = 0
        self.current_alpha = 255
        self.moved_up = False



class HealthBar:
    def __init__(self, hb_colors, player_state: dict, steps: int | None = None):
        self.__init_bars(hb_colors)
        self.__init_logic(steps)
        self.__compute_range()
        self.player_state = player_state
        self.current_state = 'neutral'
        self.rect = self.player_state[self.current_state].get_rect(midbottom=self.player_state_mount_rect.midtop)

    def redraw(self):
        ds.screen.blit(assets.Gallery.HEALTH_BAR_TEMPLATE, self.health_bar_rect)
        ds.screen.blit(self.enemy_bar, self.enemy_rect)
        ds.screen.blit(self.player_bar, self.player_rect)
        # ds.screen.blit(self.player_state_mount, self.player_state_mount_rect)
        ds.screen.blit(self.player_state[self.current_state], self.rect)

        # y = self.enemy_rect.top
        # ds.screen.blit(self.neutral_range_1, (self.half_hb_coordinates - self.neutral_range, y))
        # ds.screen.blit(self.neutral_range_2, (self.half_hb_coordinates + self.neutral_range, y))
        # ds.screen.blit(self.win_range, (self.half_hb_coordinates - self.win_or_lose_range, y))
        # ds.screen.blit(self.lose_range, (self.half_hb_coordinates + self.win_or_lose_range, y))

    def modify_health(self, flag):
        if flag == "increase":
            self.player_bar.set_alpha(255)

            if self.out_of_health:
                self.out_of_health = False
                self.player_bar.set_alpha(255)

            elif self.player_rect.width + self.pixel_per_step >= self.enemy_bar.get_width():
                self.player_rect.width = self.enemy_rect.width

            else:
                self.player_rect.width += self.pixel_per_step

        elif flag == "decrease":
            if self.player_rect.width - self.pixel_per_step > 0:
                self.player_rect.width -= self.pixel_per_step
                self.player_bar.set_alpha(255)

            else:
                self.out_of_health = True
                self.player_bar.set_alpha(0)

        padding = 5
        self.player_bar = pg.transform.smoothscale(self.player_bar, self.player_rect.size)
        self.player_rect.right = self.health_bar_rect.right - round(padding * const.HEALTHBAR_SCALE)
        self.player_state_mount_rect = self.player_state_mount.get_rect(midleft=(self.player_rect.left + self.distance_from_pb_right, self.player_rect.centery))
        self.rect = self.player_state[self.current_state].get_rect(midbottom=self.player_state_mount_rect.midtop)
        self.check_health()

    def check_health(self):
        if self.player_rect.left < self.half_hb_coordinates:
            self.__check_winning()
        elif self.player_rect.left > self.half_hb_coordinates:
            self.__check_losing()

    def __check_winning(self):
        if self.player_rect.left > self.half_hb_coordinates - self.neutral_range:
            self.current_state = 'neutral'
        elif self.player_rect.left > self.half_hb_coordinates - self.win_or_lose_range:
            self.current_state = 'winning'

    def __check_losing(self):
        if self.player_rect.left < self.half_hb_coordinates + self.neutral_range:
            self.current_state = 'neutral'
        elif self.player_rect.left < self.half_hb_coordinates + self.win_or_lose_range:
            self.current_state = 'losing'

    def __init_bars(self, hb_colors):
        self.health_bar_rect = assets.Gallery.HEALTH_BAR_TEMPLATE.get_rect(center=(const.HALF_WIDTH, 600))

        health_bar_width, health_bar_height = assets.Gallery.HEALTH_BAR_TEMPLATE.get_size()
        rect_midright_x, rect_midright_y = self.health_bar_rect.midright

        border_size = 10
        padding = 5

        self.player_bar = pg.Surface(
            (
                (health_bar_width - round(border_size * const.HEALTHBAR_SCALE))/2,
                health_bar_height - round(border_size * const.HEALTHBAR_SCALE))
        )
        self.enemy_bar = pg.Surface(
            (
                health_bar_width - round(border_size * const.HEALTHBAR_SCALE),
                health_bar_height - round(border_size * const.HEALTHBAR_SCALE)
            )
        )

        self.player_rect = self.player_bar.get_rect(
            midright=(
                rect_midright_x - round(padding * const.HEALTHBAR_SCALE),
                rect_midright_y
            )
        )
        self.enemy_rect = self.enemy_bar.get_rect(
            midright=(
                rect_midright_x - round(padding * const.HEALTHBAR_SCALE),
                rect_midright_y
            )
        )
        self.player_bar.fill(hb_colors.player)
        self.enemy_bar.fill(hb_colors.enemy)

    def __init_logic(self, steps: int | None = None):
        self.out_of_health = False

        unoccupied_part = self.enemy_bar.get_width() - self.player_bar.get_width()
        self.steps = steps if steps is not None else fun.largest_divisor(unoccupied_part, lowest_range=15, highest_range=40, start=40)
        self.pixel_per_step = self.enemy_bar.get_width() / self.steps

        self.distance_from_pb_right = 50
        self.player_state_mount = pg.Surface((10, self.player_bar.get_height() + 50))
        self.player_state_mount_rect = self.player_state_mount.get_rect(midleft=(self.player_rect.left + self.distance_from_pb_right, self.player_rect.centery))
        self.player_state_mount.fill("Gray")

    def __compute_range(self):
        neutral_range_percentage = 30
        win_or_lost_percentage = 50
        half_hb = self.enemy_bar.get_width() // 2

        self.half_hb_coordinates = self.player_rect.left
        self.neutral_range = (neutral_range_percentage * half_hb) // 100
        self.win_or_lose_range = (win_or_lost_percentage * half_hb) // 100

        # height = self.player_bar.get_height()
        # self.neutral_range_1 = pg.Surface((2, height))
        # self.neutral_range_1.fill('Blue')

        # self.neutral_range_2 = pg.Surface((2, height))
        # self.neutral_range_2.fill('Red')

        # self.win_range = pg.Surface((2, height))
        # self.win_range.fill('Green')

        # self.lose_range = pg.Surface((2, height))
        # self.lose_range.fill('Orange')



class GameLogic:
    def __init__(self, objs, player_arrow_set, enemy_arrow_set, health_bar: HealthBar):
        self.menu_score_font = assets.CustomFont.get_font("vrc-osd", const.MENU_SCORE)
        self.objs = objs
        self.player_arrow_set = player_arrow_set
        self.enemy_arrow_set = enemy_arrow_set
        self.collision_list = []
        self.copy_list = []
        self.collision_threshold = 5
        self.collision_counter = 0

        self.score = 0
        padding = 10

        self.display_stat = self.menu_score_font.render(f"Score: {self.score}", True, 'White')
        self.display_stat_rect = self.display_stat.get_rect(midbottom=(const.PLAYER_ARROW_SET_X, const.HEIGHT - padding))

        self.health_bar = health_bar

    def message_animation(self):
        for message in self.copy_list[:]:
            if message.moved_up:
                self.__perform_lerp_down(message)
                continue

            message.current_vel = fun.lerp(message.goal_vel, message.current_vel)
            message.rect.centery -= message.current_vel

            ds.screen.blit(message.surf, message.rect)

            if message.current_vel == message.goal_vel:
                message.moved_up = True

    def redraw(self, activate_main_game):
        padding = 10

        if activate_main_game:
            for obj in self.objs:
                if obj.arrow_rect.top > const.HEIGHT:
                    obj.move()
                    continue

                obj.draw_self()
                obj.move()

                # object goes offscreen
                if obj.rect.y <= - obj.surface.get_height():
                    self.copy_list.append(GameMessage('bad', self.player_arrow_set, 15, 0))
                    self.health_bar.modify_health('decrease')
                    assets.Audio.MISS_NOTE_SOUND[randint(0, 2)].play()
                    self.objs.remove(obj)

                if obj.collide_for_enemy(self.enemy_arrow_set):
                    self.objs.remove(obj)
                    break

        self.display_stat = self.menu_score_font.render(f"Score: {self.score}", True, 'White')
        self.display_stat_rect = self.display_stat.get_rect(midbottom=(const.PLAYER_ARROW_SET_X, const.HEIGHT - padding))

        ds.screen.blit(self.display_stat, self.display_stat_rect)
        self.message_animation()
        self.health_bar.redraw()

    def check_collide_player(self, key):
        if not self.collision_list and key is not None:
            self.copy_list.append(GameMessage('bad', self.player_arrow_set, 15, 0))
            assets.Audio.MISS_NOTE_SOUND[randint(0, 2)].play()
            self.health_bar.modify_health('decrease')
            return

        for obj in self.collision_list:
            if key != obj.key:

                if obj == self.collision_list[-1]:
                    self.copy_list.append(GameMessage(obj.message, self.player_arrow_set, 15, 0))
                    self.collision_list = []
                    assets.Audio.MISS_NOTE_SOUND[randint(0, 2)].play()
                    self.health_bar.modify_health('decrease')
                    return

                continue

            self.score += obj.score_earned
            self.health_bar.modify_health('increase')
            self.copy_list.append(GameMessage(obj.message, self.player_arrow_set, 15, 0))
            self.collision_list = []
            self.objs.remove(obj)
            break

    def detect_collision(self):
        for obj in self.objs:
            check = obj.collide(self.player_arrow_set)

            if check and self.collision_counter < self.collision_threshold:
                self.collision_list.append(obj)
                self.collision_counter += 1

        self.collision_counter = 0

    def __perform_lerp_down(self, message):
        message.goal_vel = 15
        message.current_vel = fun.lerp(message.goal_vel, message.current_vel)
        message.current_alpha = fun.lerp(message.goal_alpha, message.current_alpha, 13)

        message.rect.centery += message.current_vel
        message.surf.set_alpha(message.current_alpha)

        ds.screen.blit(message.surf, message.rect)

        if message.surf.get_alpha() <= 25 or message.rect.bottom >= const.HEIGHT:
            self.copy_list.remove(message)



class Intro:
    def __init__(self):
        self.load = (
            (assets.Audio.INTRO_3, assets.Gallery.THREE),
            (assets.Audio.INTRO_2, assets.Gallery.TWO),
            (assets.Audio.INTRO_1, assets.Gallery.ONE),
            (assets.Audio.INTRO_GO, assets.Gallery.GO),
        )

        self.done_playing = False

        self.index = 0
        self.current_audio = self.load[self.index][0]

        self.current_alpha = 255
        self.alpha_step = 7

        self.current_text = self.load[self.index][1]
        self.rect = self.current_text.get_rect(center=(const.HALF_WIDTH, const.HALF_HEIGHT))

        self.played = self.reached_goal = False
        self.delay = 2000
        self.run = False

        self.current_time = 0
        self.activate_time = 0

    def play(self):
        self.current_time = pg.time.get_ticks()

        if self.current_time - self.activate_time >= self.delay:
            if not self.played:
                self.played = True
                self.current_audio.play()

            ds.screen.blit(self.current_text, self.rect)
            self.alpha()

            if self.current_text.get_alpha() <= 0:
                if self.index >= len(self.load) - 1:
                    self.done_playing = True
                    self.reset()
                    return

                self.index += 1
                self.current_alpha = 255
                self.played = False
                self.current_audio = self.load[self.index][0]
                self.current_text = self.load[self.index][1]

    def alpha(self):
        self.current_alpha -= self.alpha_step
        self.current_text.set_alpha(self.current_alpha)

    def reset(self):
        self.index = 0
        self.current_audio = self.load[self.index][0]
        self.current_text = self.load[self.index][1]
        self.current_alpha = 255
        self.played = False