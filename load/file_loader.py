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
        raise Exception(f'invalid header file detected: {entry}\nconsider inspect it before running the game.') from e

    return files


def description_parser(files: list[dict]) -> list[Track]:
    return [
        Track(file["description"]["name"], file["description"]
              ["difficulties"], file["description"]["score"])
        for file in files
        if "description" in file
    ]
