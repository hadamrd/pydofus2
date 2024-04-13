import asyncio

from Cytrus import Cytrus
from data_models import AssetMetaData, GameModel


class GameData:
    def __init__(self, platforms):
        self.platforms = platforms


class Platform:
    def __init__(self, beta, main):
        self.beta = beta
        self.main = main


async def main():
    print("Loading config...")
    c = Cytrus()
    c.initialize()

    if c.cytrus_data.incomingReleasedGames:
        print(f"1: Available games : {len(c.json['Games'])}")
        print(f"2: Available IncomingReleasedGames : {len(c.json['IncomingReleasedGames'])}")
        while True:
            choice = input("Please select a choice, which list of games do you wanna chose? ")
            if choice not in ["1", "2"]:
                print("Invalid choice.")
                continue
            break

        if choice == "1":
            await select_game(False, c)
        else:
            await select_game(True, c)
    else:
        await select_game(False, c)

    print("Program terminated, press any key to exit.")
    input()


async def select_game(unreleased_games, c: Cytrus):
    games_dict = create_game_choices_list(
        c.cytrus_data.incomingReleasedGames if unreleased_games else c.cytrus_data.games
    )
    for key, value in games_dict.items():
        print(f"{key}: {value[0]}")

    while True:
        choice = input("Please select a game from the list on top: ")
        try:
            real_choice = int(choice)
            if real_choice > len(games_dict) or real_choice <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid choice.")

    await select_platform(games_dict[real_choice][0], games_dict[real_choice][1], c)


async def select_platform(game, data: GameModel, c):
    platform_dict = create_platform_choices_list(data.platforms)
    for key, value in platform_dict.items():
        print(f"{key}: {value[0]}")

    while True:
        choice = input("Please select a platform from the list on top: ")
        try:
            real_choice = int(choice)
            if real_choice > len(platform_dict) or real_choice <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid choice.")

    await select_game_version(game, platform_dict[real_choice][0], platform_dict[real_choice][1], c)


async def select_game_version(game, platform: str, platform_info: AssetMetaData, c: Cytrus):
    dict = {1: ("beta", platform_info.beta), 2: ("main", platform_info.main)}
    dict[3] = ("custom", "you choose the custom version")

    for key, value in dict.items():
        print(f"{key}: {value[0]} = {value[1]}")

    while True:
        choice = input("Please select a version from the list on top: ")
        try:
            real_choice = int(choice)
            if real_choice > len(dict) or real_choice <= 0:
                raise ValueError(f"Invalid choice. Please select a number between 1 and {len(dict)}.")
            break
        except ValueError:
            print("Invalid choice.")

    build, version = dict[real_choice]
    if real_choice == len(dict):  # last choice, the custom one
        build = input("Please write your custom version's build: ")
        version = input("Please write your custom version: ")

    await c.download_game(game, platform, build, version)


def create_platform_choices_list(dict):
    return {i + 1: (key, Platform(beta="beta1", main="main1")) for i, key in enumerate(dict)}


def create_game_choices_list(dict):
    return {i + 1: (key, GameData(platforms={"PC": "Platform data"})) for i, key in enumerate(dict)}


if __name__ == "__main__":
    asyncio.run(main())
