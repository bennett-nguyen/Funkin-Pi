import pygame
from sys import exit
from game_loader import DisplaySurf, Audio, Font, Gallery
from game_components import Surface, ImageAnimation, description_parser, file_parser

pygame.init()

week_score = 0

# ----------------
# Parent
top_rectangle = Surface(DisplaySurf.WIDTH/2, 150, DisplaySurf.WIDTH - 150, 200, (249, 209, 81))

# Child
choose_your_track = Font.TITLE_FONT_2.render("CHOOSE YOUR TRACK", True, "Black")
cyt_rect = choose_your_track.get_rect(center = top_rectangle.rect.center)

score_text = Font.MENU_SCORE.render(f"SCORE: {week_score}", True, "White")
st_rect = score_text.get_rect(midleft = (top_rectangle.rect.midleft[0], 25))
# ----------------

# ----------------
# Parent
some_rectangle = Surface(DisplaySurf.WIDTH/2, 470, 270, 300)

# Child
pointer = ImageAnimation(Gallery.POINTER, some_rectangle.rect.centerx + 250, some_rectangle.rect.centery, 0.03)
tracks = description_parser(file_parser())
# ----------------

# --- Effects
fade = pygame.Surface(DisplaySurf.Screen.get_size())
fade.fill((0, 0, 0))
fade_alpha = 255
# ---


def draw_tracks():
    distance = 0
    
    for track in tracks:
        track.init_rect_coordinates(some_rectangle.rect.centerx, some_rectangle.rect.centery + distance)
        DisplaySurf.Screen.blit(track.display_name, track.display_name_rect)
        distance += 100


def redraw():
    DisplaySurf.Screen.fill("Black")
    
    DisplaySurf.Screen.blit(top_rectangle.surface, top_rectangle.rect)
    DisplaySurf.Screen.blit(choose_your_track, cyt_rect)
    DisplaySurf.Screen.blit(score_text, st_rect)
    
    pointer.toggle_animation()
    
    draw_tracks()
    
    if fade_alpha > -1:DisplaySurf.Screen.blit(fade, (0, 0))
    pygame.display.update()



def main_menu():
    global fade_alpha

    running = True
    DisplaySurf.Clock.tick(DisplaySurf.FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        if fade_alpha > -1:
            fade.set_alpha(fade_alpha)
            fade_alpha -= 2

        redraw()

if __name__ == "__main__":
    main_menu()