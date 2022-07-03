import itertools
import pygame
import load.component as lcom
import general_component.constant as const

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
    import load.game_loader as game_loader
    from secrets import choice
    from json import load

    message_init_map = {
        "init_message": lambda text: game_loader.CustomFont.get_font(name="phantommuff-empty", size=const.TITLE_SIZE).render(text, True, "White"),
        "get_rect": lambda surf, x, y: surf.get_rect(center = (x, y))
    }

    with open("./assets/optional-message.json", "r") as f:
        file = load(f)
        message = choice(file["random"])
        result = []
        for i in range(1, 4):
            message_surf = message_init_map["init_message"](message[f"message_{i}"].upper())
            message_rect = message_init_map["get_rect"](message_surf, const.MESSAGE_X, getattr(const, f"MESSAGE_{i}_Y"))
            result.append((message_surf, message_rect))

        return result

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
