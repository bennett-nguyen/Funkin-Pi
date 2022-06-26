import itertools
import pygame
import load.component as lcom

pygame.init()

def check_presence(file):
    # assuming all of the informations are correct
    description = file["description"]
    available_difficulties = description["difficulties"]

    for difficulty in available_difficulties:
        if difficulty not in description["score"] or difficulty not in description["config"]:
            raise Exception(
                "difficulties in either score, config or mapping didn't match available difficulties")


def process_info_diff(array):
    lower_case_text = [
        difficulty.lower() for difficulty in array
    ]

    remove_junk = [
        difficulty for difficulty in list(set(lower_case_text)) if difficulty in ["easy", "normal", "hard"]
    ]
    
    return [
        string for order, string in itertools.product(("e", "n", "h"), remove_junk) if string[0] == order
    ]

def get_mapping(mapping, file):
    new_mapping = {}

    for diff_key, instruction in mapping.items():
        if type(instruction) is str and "." in instruction:
            include, diff = instruction.split(".")
            new_mapping[diff_key] = file[include][diff]
        elif type(instruction) is dict:
            new_mapping[diff_key] = instruction

    return new_mapping

def load_opt_message():
    import json
    import load.game_loader as game_loader
    
    _message_x = game_loader.DisplaySurf.WIDTH/2
    _message_1_y = game_loader.DisplaySurf.HEIGHT/2 - 150
    _message_2_y = game_loader.DisplaySurf.HEIGHT/2
    _message_3_y = game_loader.DisplaySurf.HEIGHT/2 + 150

    message_init_map = {
        "init_message": lambda text: game_loader.Font.TITLE_FONT.render(text, True, "White"),
        "get_rect": lambda surf, x, y: surf.get_rect(center = (x, y))
    }

    random_message = []
    
    with open("./assets/optional-message.json", "r") as f:
        file = json.load(f)
        
        for messages in file["random"]:
            message_surf_1 = message_init_map["init_message"](messages["message_1"].upper())
            message_surf_2 = message_init_map["init_message"](messages["message_2"].upper())
            message_surf_3 = message_init_map["init_message"](messages["message_3"].upper())
            
            message_rect_1 = message_init_map["get_rect"](message_surf_1, _message_x, _message_1_y)
            message_rect_2 = message_init_map["get_rect"](message_surf_2, _message_x, _message_2_y)
            message_rect_3 = message_init_map["get_rect"](message_surf_3, _message_x, _message_3_y)
            
            random_message.append(
                (
                    (message_surf_1, message_rect_1),
                    (message_surf_2, message_rect_2),
                    (message_surf_3, message_rect_3)
                )
            )
            
        return random_message

def file_parser() -> list[dict]:
    import json
    import os

    files = []

    for entry in os.listdir("./mapping/header"):
        if not entry.endswith(".json"):
            continue

        with open(f"./mapping/header/{entry}", "r") as f:
            file = json.load(f)
            file["description"]["difficulties"] = process_info_diff(file["description"]["difficulties"])
            
        with open(f"./mapping/header/{entry}", "w") as f:
            json.dump(file, f, indent=4)
        
        check_presence(file)
        
        file["description"]["mapping"] = get_mapping(file["description"]["mapping"], file)
        files.append(file)

    return files



def data_parser(files: list[dict]) -> list[lcom.Track]:
    return [
        lcom.Track(
            file["description"]["name"],
            file["description"]["difficulties"],
            file["description"]["score"],
            file["description"]["config"],
            file["description"]["mapping"],
            file["description"]["soundtrack"],
            file["description"]["player_animation"]
        ) 
        for file in files if "description" in file
    ]
