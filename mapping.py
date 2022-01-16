from game_components import FlyingSurf
from game_loader import DisplaySurf, Gallery
import pygame
import os
import json

pygame.init()

player_surface_x = (DisplaySurf.WIDTH/2/2)*3
enemy_surface_x = DisplaySurf.WIDTH/2/2



def file_loader() -> dict:
    if os.path.isdir(f"{os.getcwd()}\\mapping"):
        with open(f"{os.getcwd()}\\mapping\\tutorial.json", "r") as file:
            return json.load(file)

def processor(json_map: dict) -> list:
    objects = []
    distance, velocity = json_map['initial value']['distance'], json_map['initial value']['velocity']
    mapping = json_map['mapping']
    
    FlyingSurf.VEL = velocity
    temp_dist = 0
    
    for name, map in mapping.items():
        if "enemy" in name:
            for key in map:
                arrow = Gallery.ACTIVATED_LEFT_ARROW if key == 'l' else Gallery.ACTIVATED_RIGHT_ARROW if key == 'r' else  Gallery.ACTIVATED_UP_ARROW if key == 'u' else Gallery.ACTIVATED_DOWN_ARROW if key == 'd' else None
                if arrow is None:continue
                objects.append(FlyingSurf(enemy_surface_x, DisplaySurf.HEIGHT + distance + temp_dist, arrow))
                temp_dist += distance
        
        elif "player" in name:
            for key in map:
                arrow = Gallery.ACTIVATED_LEFT_ARROW if key == 'l' else Gallery.ACTIVATED_RIGHT_ARROW if key == 'r' else  Gallery.ACTIVATED_UP_ARROW if key == 'u' else Gallery.ACTIVATED_DOWN_ARROW if key == 'd' else None
                if arrow is None:continue
                objects.append(FlyingSurf(player_surface_x, DisplaySurf.HEIGHT + distance + temp_dist, arrow))
                temp_dist += distance

        elif "set" in name and map.startswith("$"):
            match map[1:map.find(":")]:
                case "distance":
                    distance = int(map[map.find(":")+1:])
                case "reset":
                    distance = json_map['initial value']['distance']

    return objects