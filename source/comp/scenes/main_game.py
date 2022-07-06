import pygame
import source.load.ds as ds
import source.load.assets as assets
import source.load.constant as const
from source.load.template import Scene
from source.load.shared import shared_data
from source.comp.other.arrow_set import ArrowSet 
from source.comp.other.main_comp import PausedScreen, GameLogic

pygame.init()

class MainGame(Scene):
    def __init__(self):
        super().__init__()
        self.redirect_delay = 1000
        self.padding = 10
        self.audio_is_playing = False
        
        self.decline_vocal_vol = False
        self.enemy_arrow_set = ArrowSet(const.ENEMY_ARROW_SET_X, 80)
        self.player_arrow_set = ArrowSet(const.PLAYER_ARROW_SET_X, 80)

        self.paused_screen_instance = PausedScreen()

        self.changed_scene_time = 0
        self.current_time = 0
        self.delay = 3000
        self.activated = False
    
    def redraw(self):
        ds.screen.fill('Black')

        # if not self.player_entity.animation_is_playable():
        #     self.player_entity.change_animation("idle")

        # self.player_entity.load_animation()
        # self.player_entity.draw_self()

        self.enemy_arrow_set.draw_self()
        self.player_arrow_set.draw_self()

        pygame.draw.line(ds.screen, "White", (const.HALF_WIDTH,0), (const.HALF_WIDTH, const.HEIGHT), 3)

        self.game_logic.redraw()
        ds.screen.blit(self.display_track_name, self.display_track_name_rect)
        
        if self.paused_screen_instance.run:
            self.paused_screen_instance.activate_pause_screen()

    def input(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.changed_scene_time >= self.delay:
            for event in shared_data.events:
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_UP:
                            self.player_arrow_set.up_arrow = assets.Gallery.ACTIVATED_UP_ARROW
                            # self.player_entity.change_animation("up")

                        case pygame.K_DOWN:
                            self.player_arrow_set.down_arrow = assets.Gallery.ACTIVATED_DOWN_ARROW
                            # self.player_entity.change_animation("down")

                        case pygame.K_LEFT:
                            self.player_arrow_set.left_arrow = assets.Gallery.ACTIVATED_LEFT_ARROW
                            # self.player_entity.change_animation("left")

                        case pygame.K_RIGHT:
                            self.player_arrow_set.right_arrow = assets.Gallery.ACTIVATED_RIGHT_ARROW
                            # self.player_entity.change_animation("right")

                        case pygame.K_p:
                            self.paused_screen_instance.run = True
                
                    self.game_logic.check_collide_player(event.key)
                elif event.type == pygame.KEYUP:
                    self.player_arrow_set.event_on_arrow_deactivate(event)
    
    def pre_event(self):
        self.current_time = pygame.time.get_ticks()

        if self.current_time - self.changed_scene_time >= self.delay:
            self.activated = True
    
    def end_pre_event(self):
        return self.activated
    
    def play_audio(self):
        self.instrument.play()
        self.vocal.play()
    
    def receive_data(self, data):
        menu_score_font = assets.CustomFont.get_font("vrc-osd", const.MENU_SCORE)

        self.track_name = data["name"]
        self.chosen_difficulty = data["chosen_difficulty"]
        self.game_delay = data["difficulty_config"]["delay"]
        self.game_logic = GameLogic(data["objects"], self.player_arrow_set, self.enemy_arrow_set)

        self.instrument = data["instrument"]
        self.vocal = data["vocal"]

        self.player_entity = data["player_entity"]

        self.display_track_name = menu_score_font.render(f"{self.track_name} - {self.chosen_difficulty}", True, "White")
        self.display_track_name_rect = self.display_track_name.get_rect(bottomleft = (self.padding, const.HEIGHT - self.padding))

    def reset_attr(self):
        super().reset_attr()
