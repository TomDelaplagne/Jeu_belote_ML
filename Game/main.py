#! /usr/bin/python3

import pandas as pd
from contextlib import redirect_stdout
from game_class import BeloteGame
from player_class import Player, Dumb_Player
from player_neural_class import Player_Neural
from json import dumps, loads
from alive_progress import alive_bar
import numpy as np
import os, sys
from scipy.optimize import minimize


def cost_function(matrices):
    # Your cost function implementation here
    Lancelot = Player_Neural("Lancelot", strategy=matrices)
    players: list[Player] = [Lancelot, Dumb_Player("Bob"), Dumb_Player("Charlie"), Dumb_Player("David")]
    game = BeloteGame(players)
    cost = 0
    NB_PARTIES = 1_000
    with alive_bar(NB_PARTIES) as bar:
        for _ in range(NB_PARTIES):
            with redirect_stdout(open(os.devnull, "w")):
                points = game.play()
            bar()
    cost += points[str(Lancelot)]
    return -cost



def get_points(index: int) -> dict:
    players: list[Player] = [Player_Neural("Lancelot"), Dumb_Player("Bob"), Dumb_Player("Charlie"), Dumb_Player("David")]
    game = BeloteGame(players)

    with redirect_stdout(open(os.devnull, "w")):
        points = game.play()

    data = {
        "indice": [index],
        f"{game.players[0]}": [points[f"{game.players[0]}"]],
        f"{game.players[1]}": [points[f"{game.players[1]}"]],
        f"{game.players[2]}": [points[f"{game.players[2]}"]],
        f"{game.players[3]}": [points[f"{game.players[3]}"]],
    }
    df = pd.DataFrame(data)
    df.to_csv('history.csv', mode='a', index=False, header=(index == 1))
    return data

def main(args=None):
    with open(f'history.csv', "w") as f:
        f.write("")
    with open(f'points', "w") as f:
        f.write("{}")
    NB_PARTIES = 10_000


    if os.path.isfile("strategy.npy"):
        matrices = np.load("strategy.npy")
    else:
        matrix1 = np.random.rand(32,16)
        matrix2 = np.random.rand(16,16)
        matrix3 = np.random.rand(16,1)
        matrices = [matrix1, matrix2, matrix3]

    x0 = np.concatenate([matrices[0].flatten(), matrices[1].flatten(), matrices[2].flatten()])
    res = minimize(cost_function, x0, method='BFGS')
    print(res)
    np.save("strategy.npy", res)

    with alive_bar(NB_PARTIES) as bar:
        for i in range(1,NB_PARTIES+1):
            _ = get_points(i)
            bar()

if __name__ == "__main__":
    main(args=None)