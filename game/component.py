from email import message
import pygame
import load.game_loader as game_loader
import general_component.component as gcom
import cv2

pygame.init()

class ArrowSet(gcom.Surface):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH/2/1.3, 70)

        self.left_arrow = game_loader.Gallery.LEFT_ARROW
        self.up_arrow = game_loader.Gallery.UP_ARROW
        self.down_arrow = game_loader.Gallery.DOWN_ARROW
        self.right_arrow = game_loader.Gallery.RIGHT_ARROW

        self.left_arrow_rect = self.left_arrow.get_rect(
            midleft=(self.rect.midleft[0] + 25, self.rect.midleft[1]))
        self.down_arrow_rect = self.down_arrow.get_rect(
            midleft=(self.rect.midleft[0] + 135, self.rect.midleft[1]))
        self.up_arrow_rect = self.up_arrow.get_rect(
            midright=(self.rect.midright[0] - 135, self.rect.midright[1]))
        self.right_arrow_rect = self.right_arrow.get_rect(
            midright=(self.rect.midright[0] - 25, self.rect.midright[1]))

        self.arrow_list = ((self.left_arrow, self.left_arrow_rect), (self.up_arrow, self.up_arrow_rect), (
            self.down_arrow, self.down_arrow_rect), (self.right_arrow, self.right_arrow_rect))

    def update_arrows(self):
        self.arrow_list = ((self.left_arrow, self.left_arrow_rect), (self.up_arrow, self.up_arrow_rect), (
            self.down_arrow, self.down_arrow_rect), (self.right_arrow, self.right_arrow_rect))

    def draw_self(self):
        self.update_arrows()

        for object in self.arrow_list:
            game_loader.DisplaySurf.Screen.blit(
                object[0], object[1])

    def event_on_arrow_deactivate(self, event):
        match event.key:
            case pygame.K_UP:
                self.up_arrow = game_loader.Gallery.UP_ARROW

            case pygame.K_DOWN:
                self.down_arrow = game_loader.Gallery.DOWN_ARROW

            case pygame.K_LEFT:
                self.left_arrow = game_loader.Gallery.LEFT_ARROW

            case pygame.K_RIGHT:
                self.right_arrow = game_loader.Gallery.RIGHT_ARROW


class FlyingObject(gcom.Surface):
    def __init__(self, x: int, y: int, arrow, VEL) -> None:
        super().__init__(x, y, game_loader.DisplaySurf.WIDTH/(13/5), 70)
        self.VEL = VEL
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
        game_loader.DisplaySurf.Screen.blit(self.arrow, self.arrow_rect)

    def move(self):
        rect_vel_y = self.rect.y
        arrow_rect_vel_y = self.arrow_rect.y

        rect_vel_y -= round(self.VEL * game_loader.shared_data.dt)
        arrow_rect_vel_y -= round(self.VEL * game_loader.shared_data.dt)

        self.rect.y = rect_vel_y
        self.arrow_rect.y = arrow_rect_vel_y

    def collide(self, object):
        # range from object.rect.center[1] + range --> object.rect.center[1] - range
        # the shorter the range, the harder you'll get a sick move
        range = 8
        target = self.rect
        lowest_center_range = object.rect.center[1] - range
        highest_center_range = object.rect.center[1] + range

        score_earned = 25
        sick_earned = 60

        if target.center[1] >= lowest_center_range and target.center[1] <= highest_center_range and target.colliderect(object.rect):
            return (True, 'sick', sick_earned)
        elif target.colliderect(object.rect):
            return (True, 'good', score_earned)
        else:
            return [False]

    # this method is only used for the enemy!
    def collide_for_enemy(self, object):
        return self.rect.center[1] <= object.rect.center[1] and self.rect.colliderect(object)

class Entity(gcom.Surface):

    def __init__(self, is_player: bool, video_path) -> None:
        x = game_loader.DisplaySurf.WIDTH/4

        if is_player:
            x = (game_loader.DisplaySurf.WIDTH/4)*3

        super().__init__(x, game_loader.DisplaySurf.HEIGHT/2, game_loader.DisplaySurf.WIDTH /
                         2, game_loader.DisplaySurf.HEIGHT)

        self.video_path = video_path
        self.state = cv2.VideoCapture(self.video_path["idle"])

    def animation_is_playable(self):
        success, _ = self.state.read()
        return success

    def change_animation(self, animation):
        '''
        animation type: idle, left, up, down, right
        '''
        self.state = cv2.VideoCapture(self.video_path[animation])

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

class GameMessage:
    def __init__(self, message_code, player_arrow_set, vel, goal):
        match message_code:
            case "sick":
                self.surf = game_loader.Gallery.SICK.copy()
                self.rect = game_loader.Gallery.SICK.get_rect(center = (game_loader.DisplaySurf.WIDTH/2 + 10, player_arrow_set.rect.centery + 100))
            case "good":
                self.surf = game_loader.Gallery.GOOD.copy()
                self.rect = game_loader.Gallery.GOOD.get_rect(center = (game_loader.DisplaySurf.WIDTH/2, player_arrow_set.rect.centery + 100))
            case "bad":
                self.surf = game_loader.Gallery.BAD.copy()
                self.rect = game_loader.Gallery.GOOD.get_rect(center = (game_loader.DisplaySurf.WIDTH/2, player_arrow_set.rect.centery + 100))

        self.goal_vel = goal
        self.current_vel = vel
        
        self.goal_alpha = 0
        self.current_alpha = 255
        self.moved_up = False

class GameLogic:
    def __init__(self, objects, player_arrow_set, enemy_arrow_set):
        self.menu_score_font = game_loader.CustomFont.get_font("vrc-osd", 20)
        self.objects = objects
        self.player_arrow_set = player_arrow_set
        self.enemy_arrow_set = enemy_arrow_set
        self.copy_list = []


        self.score = 0
        padding = 10
        player_surface_x = (game_loader.DisplaySurf.WIDTH/4)*3

        self.display_stat = self.menu_score_font.render(f"Score: {self.score}", True, 'White')
        self.display_stat_rect = self.display_stat.get_rect(midbottom = (player_surface_x, game_loader.DisplaySurf.HEIGHT - padding))

    def lerp(self, goal, current, dt=1):
        difference = goal - current
        
        if difference > dt:
            return current + dt
        elif difference < -dt:
            return current - dt
        
        return goal
    
    def message_animation(self):
        for message in self.copy_list[:]:
            if not message.moved_up:
                message.current_vel = self.lerp(message.goal_vel, message.current_vel)
                message.rect.centery -= message.current_vel
                game_loader.DisplaySurf.Screen.blit(message.surf, message.rect)
                if message.current_vel == message.goal_vel:
                    message.moved_up = True
            else:
                message.goal_vel = 15
                message.current_vel = self.lerp(message.goal_vel, message.current_vel)
                message.current_alpha = self.lerp(message.goal_alpha, message.current_alpha, 13)
                
                message.rect.centery += message.current_vel
                message.surf.set_alpha(message.current_alpha)
                
                game_loader.DisplaySurf.Screen.blit(message.surf, message.rect)
                
                if message.surf.get_alpha() <= 25 or message.rect.bottom >= game_loader.DisplaySurf.HEIGHT:
                    self.copy_list.remove(message)


    def redraw(self):
        player_surface_x = (game_loader.DisplaySurf.WIDTH/4)*3
        padding = 10

        for object in self.objects:
            if object.arrow_rect.top > game_loader.DisplaySurf.HEIGHT:
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
        self.display_stat_rect = self.display_stat.get_rect(midbottom = (player_surface_x, game_loader.DisplaySurf.HEIGHT - padding))
        
        self.message_animation()
        game_loader.DisplaySurf.Screen.blit(self.display_stat, self.display_stat_rect)

    def check_collide_player(self, key):
        for object in self.objects[:]:
            check = object.collide(self.player_arrow_set)
            
            if (not check[0]) or (check[0] and object.key != key):
                self.copy_list.append(GameMessage('bad', self.player_arrow_set, 15, 0))
                break

            self.objects.remove(object)
            self.score += check[2]
            self.copy_list.append(GameMessage(check[1], self.player_arrow_set, 15, 0))
            break