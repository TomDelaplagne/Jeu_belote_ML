#! /usr/bin/python3

import pandas as pd
from contextlib import redirect_stdout
from game_class import BeloteGame
from player_class import Player, Dumb_Player
from json import dumps, loads
from alive_progress import alive_bar
import os, sys


def get_points(index: int) -> dict:
    game = BeloteGame([Dumb_Player("Alice"), Dumb_Player("Bob"), Dumb_Player("Charlie"), Dumb_Player("David")])

    with open(f'points', "r") as f:
        points = f.read()
    points = loads(points)
    
    # try:
    #     index = len(pd.read_csv('history.csv'))
    # except:
    #     index = 0
    new_points = {}

    with redirect_stdout(open(os.devnull, "w")):
        new_points = game.play()

    for player in new_points:
        if player in points:
            points[player] += new_points[player]
        else:
            points[player] = new_points[player]

    data = {
        "indice": [index],
        f"{game.players[0]}": [points[f"{game.players[0]}"]],
        f"{game.players[1]}": [points[f"{game.players[1]}"]],
        f"{game.players[2]}": [points[f"{game.players[2]}"]],
        f"{game.players[3]}": [points[f"{game.players[3]}"]],
    }

    df = pd.DataFrame(data)
    df.to_csv('history.csv', mode='a', index=False, header=(index == 0))

    with open(f'points', "w") as f:
        f.write(dumps(points, indent=4))

    return points

def main(args=None):
    # with open(f'history.csv', "w") as f:
    #     f.write("")
    # with open(f'points', "w") as f:
    #     f.write("{}")
    if args is not None:
        NB_PARTIES = sys.argv[1:]
    else:
        NB_PARTIES = 10_000
    with alive_bar(NB_PARTIES) as bar:
        for i in range(NB_PARTIES):
            _ = get_points(i)
            bar()

if __name__ == "__main__":
    main(args=None)