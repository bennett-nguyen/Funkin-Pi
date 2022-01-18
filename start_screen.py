import pygame
from game_loader import Gallery, DisplaySurf, Audio
from game_components import Surface, ImageAnimation

pygame.init()
pygame.display.set_caption("Friday Night Funkin' - At Home")

Audio.FREAKY_MENU.play(-1)
button_pressed = False
sound_effect_played = False

deactivated_button = ImageAnimation(Gallery.BUTTON_DEACTIVATED_IMAGES, DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT/2 + 270, 0.1)
on_hover_button = ImageAnimation(Gallery.BUTTON_ON_HOVER_IMAGES, DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT/2 + 270, 0.1)
activated_button = ImageAnimation(Gallery.BUTTON_ACTIVATED_IMAGES, DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT/2 + 270, 0.15)

button_hit_box = Surface(DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT/2 + 270, 250, 120)

def draw_window():
    global button_pressed
    DisplaySurf.Screen.fill('Black')

    DisplaySurf.Screen.blit(Gallery.LOGO, Gallery.LOGO.get_rect(center = (DisplaySurf.WIDTH/2, DisplaySurf.HEIGHT/2)))
    DisplaySurf.Screen.blit(button_hit_box.surface, button_hit_box.rect)

    if (
        pygame.mouse.get_pressed()[0]
        and button_hit_box.rect.collidepoint(pygame.mouse.get_pos())
        and not button_pressed
    ):
        button_pressed = True

    if button_pressed:
        activated_button.toggle_animation()

    if not button_pressed:
        if button_hit_box.rect.collidepoint(pygame.mouse.get_pos()):
            on_hover_button.toggle_animation()
        else:
            deactivated_button.toggle_animation()

    pygame.display.update()
    return button_pressed

def start_screen():
    global sound_effect_played, button_pressed
    running = True
    
    while running:
        DisplaySurf.Clock.tick(DisplaySurf.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                button_pressed = True
                
        if button_pressed and not sound_effect_played:
            Audio.CONFIRM_MENU.play()
            sound_effect_played = True
        
        draw_window()

start_screen()