import pygame
from load.component import Track

pygame.init()


def file_parser() -> list[dict]:
    import json
    import os
    files = []

    try:
        for entry in os.listdir("./mapping/header"):
            if not entry.endswith(".json"):
                continue

            with open(f"./mapping/header/{entry}", "r") as f:
                file = json.load(f)
                files.append(file)
    except Exception as e:
        print("an exception occurred during runtime:")
        print(e)
        raise Exception(
            f'invalid header file detected: {entry}\nconsider inspect it before running the game.') from e

    return files


def make_text_lowercase(array):
    return [
        difficulty.lower() for difficulty in array
    ]


def remove_junk(array):
    return [
        difficulty for difficulty in array if difficulty in ["easy", "normal", "hard"]
    ]


def description_parser(files: list[dict]) -> list[Track]:

    return [
        Track(file["description"]["name"],
            list(set(
                remove_junk(
                    make_text_lowercase(file["description"]["difficulties"])))
                ),
            file["description"]["score"])

        for file in files
        if "description" in file
    ]
