import pygame
import itertools
from source.comp.json.comp import Track

pygame.init()


def _check_presence(file):
    # assuming all of the informations are correct
    description = file["description"]
    available_difficulties = description["difficulties"]

    for difficulty in available_difficulties:
        if difficulty not in description["score"] or difficulty not in description["config"]:
            raise AttributeError("difficulties in either score, config or mapping didn't match available difficulties")


def _process_info_diff(array):
    lower_case_text = [
        difficulty.lower() for difficulty in array
    ]

    remove_junk = [
        difficulty for difficulty in list(set(lower_case_text)) if difficulty in ["easy", "normal", "hard"]
    ]
    
    return [
        string for order, string in itertools.product(("e", "n", "h"), remove_junk) if string[0] == order
    ]


def _get_mapping(mapping, file):
    new_mapping = {}

    for diff_key, instruction in mapping.items():
        if type(instruction) is str and "." in instruction:
            include, diff = instruction.split(".")
            new_mapping[diff_key] = file[include][diff]
        elif type(instruction) is dict:
            new_mapping[diff_key] = instruction

    return new_mapping


def file_parser() -> list[dict]:
    import json
    import os

    files = []

    for entry in os.listdir("./mapping/header"):
        if not entry.endswith(".json"):
            continue

        with open(f"./mapping/header/{entry}", "r") as f:
            file = json.load(f)
            file["description"]["difficulties"] = _process_info_diff(file["description"]["difficulties"])
            
        with open(f"./mapping/header/{entry}", "w") as f:
            json.dump(file, f, indent=4)
        
        _check_presence(file)
        
        file["description"]["mapping"] = _get_mapping(file["description"]["mapping"], file)
        files.append(file)

    return files

def data_parser(files: list[dict]) -> list[Track]:
    return [
        Track(
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