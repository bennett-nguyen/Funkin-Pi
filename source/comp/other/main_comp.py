import pygame
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
from sys import exit
from random import randint
from source.comp.other.button import Button

pygame.init()


class PausedScreen:
    def __init__(self):
        self.background = pygame.Surface((1200, 690))
        self.background.fill("Grey")
        self.background.set_alpha(15)
        self.play_sfx_1 = False
        self.play_sfx_2 = False
        
        self.paused_background = assets.Gallery.PAUSED_BACKGROUND
        self.paused_background_rect = self.paused_background.get_rect(center = (const.HALF_WIDTH, const.HALF_HEIGHT))

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            self._check_hover()
            self.continue_button.check_click(click_type=0)
            if self.continue_button.activated_by_click:
                self.run = False
                ds.clock.tick(const.FPS)

            pygame.display.update()



class GameMessage:
    def __init__(self, message_code, player_arrow_set, vel, goal):
        match message_code:
            case "sick":
                self.surf = assets.Gallery.SICK.copy()
                self.rect = assets.Gallery.SICK.get_rect(center = (const.HALF_WIDTH + 10, player_arrow_set.rect.centery + 100))
            case "good":
                self.surf = assets.Gallery.GOOD.copy()
                self.rect = assets.Gallery.GOOD.get_rect(center = (const.HALF_WIDTH, player_arrow_set.rect.centery + 100))
            case "bad":
                self.surf = assets.Gallery.BAD.copy()
                self.rect = assets.Gallery.GOOD.get_rect(center = (const.HALF_WIDTH + 20, player_arrow_set.rect.centery + 100))

        self.goal_vel = goal
        self.current_vel = vel

        self.goal_alpha = 0
        self.current_alpha = 255
        self.moved_up = False



class GameLogic:
    def __init__(self, objects, player_arrow_set, enemy_arrow_set):
        self.menu_score_font = assets.CustomFont.get_font("vrc-osd", const.MENU_SCORE)
        self.objects = objects
        self.player_arrow_set = player_arrow_set
        self.enemy_arrow_set = enemy_arrow_set
        self.collision_list = []
        self.copy_list = []
        self.collision_threshold = 5
        self.collision_counter = 0

        self.score = 0
        padding = 10

        self.display_stat = self.menu_score_font.render(f"Score: {self.score}", True, 'White')
        self.display_stat_rect = self.display_stat.get_rect(midbottom = (const.PLAYER_ARROW_SET_X, const.HEIGHT - padding))

    def lerp(self, goal, current, dt=1):
        difference = goal - current
        
        if difference > dt:
            return current + dt
        elif difference < -dt:
            return current - dt
        
        return goal

    def message_animation(self):
        for message in self.copy_list[:]:
            if message.moved_up:
                self.__perform_lerp_down(message)
                continue

            message.current_vel = self.lerp(message.goal_vel, message.current_vel)
            message.rect.centery -= message.current_vel

            ds.screen.blit(message.surf, message.rect)

            if message.current_vel == message.goal_vel:
                message.moved_up = True

    def redraw(self, activate_main_game):
        padding = 10

        if activate_main_game:
            for object in self.objects:
                if object.arrow_rect.top > const.HEIGHT:
                    object.move()
                    continue

                object.draw_self()
                object.move()

                # object goes offscreen
                if object.rect.y <= - object.surface.get_height():
                    self.copy_list.append(GameMessage('bad', self.player_arrow_set, 15, 0))
                    self.objects.remove(object)

                if object.collide_for_enemy(self.enemy_arrow_set):
                    self.objects.remove(object)
                    break

        self.display_stat = self.menu_score_font.render(f"Score: {self.score}", True, 'White')
        self.display_stat_rect = self.display_stat.get_rect(midbottom = (const.PLAYER_ARROW_SET_X, const.HEIGHT - padding))
        
        self.message_animation()
        ds.screen.blit(self.display_stat, self.display_stat_rect)

    def check_collide_player(self, key):
        if not self.collision_list and key is not None:
            self.copy_list.append(GameMessage('bad', self.player_arrow_set, 15, 0))
            assets.Audio.MISS_NOTE_SOUND[randint(0, 2)].play()
            return

        for object in self.collision_list:
            if key != object.key:

                if object == self.collision_list[-1]:
                    self.copy_list.append(GameMessage('bad', self.player_arrow_set, 15, 0))
                    self.collision_list = []
                    assets.Audio.MISS_NOTE_SOUND[randint(0, 2)].play()
                    return

                continue

            self.score += object.score_earned
            self.copy_list.append(GameMessage(object.message, self.player_arrow_set, 15, 0))
            self.collision_list = []
            self.objects.remove(object)
            break

    def detect_collision(self):
        for object in self.objects:
            check = object.collide(self.player_arrow_set)

            if check and self.collision_counter < self.collision_threshold:
                self.collision_list.append(object)
                self.collision_counter += 1

        self.collision_counter = 0

    def __perform_lerp_down(self, message):
        message.goal_vel = 15
        message.current_vel = self.lerp(message.goal_vel, message.current_vel)
        message.current_alpha = self.lerp(message.goal_alpha, message.current_alpha, 13)

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
        self.rect = self.current_text.get_rect(center = (const.HALF_WIDTH, const.HALF_HEIGHT))

        self.played = self.reached_goal = False
        self.delay = 2000
        self.run = False
        
        self.current_time = 0
        self.activate_time = 0

    def play(self):
        self.current_time = pygame.time.get_ticks()
        
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