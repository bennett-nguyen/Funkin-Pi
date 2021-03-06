import pygame
import load.game_loader as game_loader
import general_component.component as genc
import game.component as game_component
from load.game_loader import Data
from scene.component import MenuLogic, Scene, PausedScreen

pygame.init()

class StartScreen(Scene):
    def __init__(self):
        super().__init__()
        self.sound_1_effect_played = self.sound_2_effect_played = self.button_pressed = False

        self.redirect_delay = 3500
        self.fade_delay = 2500

        # custom fade in animation
        self.surf = pygame.Surface(game_loader.DisplaySurf.Screen.get_size())
        self.surf.fill((255, 255, 255))

        self.alpha = 255
        # ----

        self.deactivated_button = genc.ImageAnimation(
            game_loader.Gallery.PLAY_BUTTON_DEACTIVATED_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.1)
        self.on_hover_button = genc.ImageAnimation(
            game_loader.Gallery.PLAY_BUTTON_ON_HOVER_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.1)
        self.activated_button = genc.ImageAnimation(
            game_loader.Gallery.PLAY_BUTTON_ACTIVATED_IMAGES, game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 0.15)
        self.button_hit_box = genc.Surface(
            game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2 + 270, 250, 120)

    def redraw(self):
        game_loader.DisplaySurf.Screen.blit(game_loader.Gallery.LOGO, game_loader.Gallery.LOGO.get_rect(
            center=(game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT/2)))

        if self.button_pressed:
            self.activated_button.toggle_animation()
            self.redirect = "menu screen"

        if not self.button_pressed:
            if self.button_hit_box.rect.collidepoint(pygame.mouse.get_pos()):
                self.on_hover_button.toggle_animation()

                if not self.sound_2_effect_played:
                    game_loader.Audio.SCROLL_MENU.play()
                    self.sound_2_effect_played = True
            else:
                self.deactivated_button.toggle_animation()
                self.sound_2_effect_played = False

        if self.alpha > -1:
            self.custom_fade_in()

    def input(self):
        if (
            pygame.mouse.get_pressed()[0]
            and self.button_hit_box.rect.collidepoint(pygame.mouse.get_pos())
        ) or (pygame.key.get_pressed()[pygame.K_RETURN]):
            self.button_pressed = True

        if self.button_pressed and not self.sound_1_effect_played:
            game_loader.Audio.CONFIRM_MENU.play()
            self.sound_1_effect_played = True

    def custom_fade_in(self):
        self.alpha -= 3
        self.surf.set_alpha(self.alpha)
        game_loader.DisplaySurf.Screen.blit(self.surf, (0, 0))

    def reset_attr(self):
        super().reset_attr()
        self.sound_1_effect_played = self.sound_2_effect_played = self.button_pressed = False


class MenuScreen(Scene):
    def __init__(self):
        super().__init__()
        self.redirect_delay = 4000
        self.fade_delay = 2900
        self.on_toggle_chosen_track = False

        self.yellow_rectangle = genc.Surface(
            game_loader.DisplaySurf.WIDTH/2, 150, game_loader.DisplaySurf.WIDTH - 150, 200, (249, 209, 81))

        self.choose_your_track = game_loader.Font.TITLE_FONT_2.render(
            "CHOOSE YOUR TRACK", True, "Black")
        self.cyt_rect = self.choose_your_track.get_rect(
            center=self.yellow_rectangle.rect.center)

        self.track_chooser_rect = genc.Surface(
            game_loader.DisplaySurf.WIDTH/2, 470, 270, 300)
        self.pointer = genc.ImageAnimation(
            game_loader.Gallery.POINTER, self.track_chooser_rect.rect.centerx + 250, self.track_chooser_rect.rect.centery, 0.1)
        self.tracks = Data.descriptions

        distance = 0

        for track in self.tracks:
            track.init_display_name_rect_coordinates(
                self.track_chooser_rect.rect.centerx, self.track_chooser_rect.rect.centery + distance)
            track.run_init()
            distance += 120

        self.logic = MenuLogic(self.tracks, self.dt)

    def redraw(self):
        self.logic.redraw()

        game_loader.DisplaySurf.Screen.blit(
            self.yellow_rectangle.surface, self.yellow_rectangle.rect)

        game_loader.DisplaySurf.Screen.blit(
            self.choose_your_track, self.cyt_rect)

        self.pointer.toggle_animation()
        
        if self.on_toggle_chosen_track:
            self.logic.current_track.display_name_animation.toggle_animation()

    def input(self):

        if self.allow_keydown:
            self.logic.input()

            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.redirect = "start screen"
                            self.allow_keydown = False

                        case pygame.K_RETURN:
                            self._key_return_event()

    def _key_return_event(self):
        self.loaded_data = self.logic.load_track_data()
        self.logic.current_track.set_animation_coordinates(self.logic.current_track.display_name_rect.centerx,
                                                          self.logic.current_track.display_name_rect.centery)
        game_loader.Audio.CONFIRM_MENU.play()
        self.on_toggle_chosen_track = True
        self.redirect = "main game"
        self.allow_keydown = False
        
    def reset_attr(self):
        super().reset_attr()
        self.loaded_data = None


class MainGame(Scene):
    def __init__(self):
        super().__init__()
        self.redirect_delay = 1000
        self.padding = 10

        self.player_surface_x = (game_loader.DisplaySurf.WIDTH/4)*3
        self.enemy_surface_x = game_loader.DisplaySurf.WIDTH/4
        
        self.enemy_arrow_set = game_component.ArrowSet(self.enemy_surface_x, 80)
        self.player_arrow_set = game_component.ArrowSet(self.player_surface_x, 80)
        
        self.score = 0
        self.display_stat = game_loader.Font.MENU_SCORE.render(f"Score: {self.score}", True, 'White')
        self.display_stat_rect = self.display_stat.get_rect(midbottom = (self.player_surface_x, game_loader.DisplaySurf.HEIGHT - self.padding))

        self.paused_screen_instance = PausedScreen()
        # self.player_entity = game_component.Entity(self.player_surface_x, game_loader.DisplaySurf.HEIGHT/2)
        # self.enemy_entity = game_component.Entity(self.enemy_surface_x, game_loader.DisplaySurf.HEIGHT/2)
        
    
    def redraw(self):
        game_loader.DisplaySurf.Screen.fill('Black')

        # if not self.player_entity.animation_is_playable():
        #     self.player_entity.change_animation(game_loader.Gallery.ENTITY_IDLE)

        # self.player_entity.load_animation()
        # self.player_entity.draw_self()
        
        self.enemy_arrow_set.draw_self()
        self.player_arrow_set.draw_self()

        pygame.draw.line(game_loader.DisplaySurf.Screen, "White", (game_loader.DisplaySurf.WIDTH/2,
                            0), (game_loader.DisplaySurf.WIDTH/2, game_loader.DisplaySurf.HEIGHT), 3)
        

        # for object in self.objects:
        #     object.draw_self()
        #     object.move()

        #     # object goes offscreen
        #     if object.rect.y <= - object.surface.get_height():
        #         self.objects.remove(object)

        #     if object.collide_for_enemy(self.enemy_arrow_set):
        #         self.objects.remove(object)

        #         break
        game_loader.DisplaySurf.Screen.blit(self.display_stat, self.display_stat_rect)
        game_loader.DisplaySurf.Screen.blit(self.display_track_name, self.display_track_name_rect)
        
        if self.paused_screen_instance.run:
            self.paused_screen_instance.activate_pause_screen()

        pygame.display.update()

    def input(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.player_arrow_set.up_arrow = game_loader.Gallery.ACTIVATED_UP_ARROW

                    case pygame.K_DOWN:
                        self.player_arrow_set.down_arrow = game_loader.Gallery.ACTIVATED_DOWN_ARROW

                    case pygame.K_LEFT:
                        self.player_arrow_set.left_arrow = game_loader.Gallery.ACTIVATED_LEFT_ARROW

                    case pygame.K_RIGHT:
                        self.player_arrow_set.right_arrow = game_loader.Gallery.ACTIVATED_RIGHT_ARROW
                    
                    case pygame.K_p:
                        self.paused_screen_instance.run = True
            
            elif event.type == pygame.KEYUP:
                self.player_arrow_set.event_on_arrow_deactivate(event)
                        
    
    def receive_data(self, data):
        self.track_name = data["name"]
        self.chosen_difficulty = data["chosen_difficulty"]
        self.game_delay = data["difficulty_config"]["delay"]
        self.objects = data["objects"]
        
        self.display_track_name = game_loader.Font.MENU_SCORE.render(f"{self.track_name} - {self.chosen_difficulty}", True, "White")
        self.display_track_name_rect = self.display_track_name.get_rect(bottomleft = (self.padding, game_loader.DisplaySurf.HEIGHT - self.padding))
        
    def reset_attr(self):
        super().reset_attr()
