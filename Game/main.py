#! /usr/bin/python3

import pandas as pd
from contextlib import redirect_stdout
from game_class import BeloteGame
from player_class import Player, Dumb_Player
from player_neural_class import Player_Neural
from alive_progress import alive_bar
import numpy as np
import os
import copy
from scipy.optimize import minimize
from deck_class import Deck

def cost_function(matrices):
    # Your cost function implementation here
    global idx
    NB_PARTIES = len(list_of_decks)
    results = []
    current_deck_list = [None] * NB_PARTIES
    for i in range(NB_PARTIES):
        current_deck_list[i] = copy.deepcopy(list_of_decks[i])

    # with alive_bar(NB_PARTIES) as bar:
    for deck in current_deck_list:
        with redirect_stdout(open(os.devnull, "w")):
            Lancelot = Player_Neural("Lancelot", strategy=matrices)
            Lancelot2 = Player_Neural("Lancelot2", strategy=matrices)
            players: list[Player] = [Lancelot, Dumb_Player("Bob"), Lancelot2, Dumb_Player("David")]
            game = BeloteGame(players, deck)
            points = game.play()
            # bar()
            results.append(points[str(Lancelot)])
    # with open("played.txt", "a") as file:
    #     file.write(f"{np.sum(np.square(matrices)) / 2}\n")
    cost = -np.mean(results)
    idx += 1
    if idx%100 == 0:
        print(-cost, idx)
    return cost

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
    NB_PARTIES = 1
    INPUT_NEURONS = 32
    FIRST_LAYER_HIDDEN_NEURONS = 16
    SECOND_LAYER_HIDDEN_NEURONS = 16
    output_neurons = 1

    # if os.path.isfile("strategy.npy"):
    #     # x0 = np.load("strategy.npy")
    # else:
    matrix1 = np.random.normal(0, INPUT_NEURONS**-0.5,(INPUT_NEURONS, FIRST_LAYER_HIDDEN_NEURONS))
    matrix2 = np.random.normal(0, FIRST_LAYER_HIDDEN_NEURONS**-0.5, (FIRST_LAYER_HIDDEN_NEURONS, SECOND_LAYER_HIDDEN_NEURONS))
    matrix3 = np.random.normal(0, SECOND_LAYER_HIDDEN_NEURONS**-0.5, (SECOND_LAYER_HIDDEN_NEURONS, output_neurons))
    first_hidden_bias = np.zeros(FIRST_LAYER_HIDDEN_NEURONS)
    second_hidden_bias = np.zeros(SECOND_LAYER_HIDDEN_NEURONS)
    output_bias = np.zeros(output_neurons)
    x0 = np.concatenate([matrix1.flatten(), matrix2.flatten(), matrix3.flatten(), first_hidden_bias, second_hidden_bias, output_bias])

    matrix1_bounds = [(-1,1) for _ in range(INPUT_NEURONS * FIRST_LAYER_HIDDEN_NEURONS)]
    matrix2_bounds = [(-1, 1) for _ in range(FIRST_LAYER_HIDDEN_NEURONS * SECOND_LAYER_HIDDEN_NEURONS)]
    matrix3_bounds = [(-1, 1) for _ in range(SECOND_LAYER_HIDDEN_NEURONS * output_neurons)]
    bias_bounds = [(None, None) for _ in range(FIRST_LAYER_HIDDEN_NEURONS+SECOND_LAYER_HIDDEN_NEURONS+output_neurons)]

    global list_of_decks
    list_of_decks = []
    print("Generating decks...")
    with alive_bar(NB_PARTIES) as bar:
        for _ in range(NB_PARTIES):
            list_of_decks.append(Deck())
            bar()
    # x0 = np.concatenate([matrix1.flatten(), matrix2.flatten(), matrix3.flatten(), first_hidden_bias, second_hidden_bias, output_bias])
    # print(cost_function(x0))

    bounds_of_x0 = matrix1_bounds + matrix2_bounds + matrix3_bounds + bias_bounds

    global idx
    idx = 0
    res = minimize(cost_function, x0, method='Nelder-Mead', bounds=bounds_of_x0, options={'disp': True, 'adaptive': False})
    np.save("strategy.npy", res.x)

if __name__ == "__main__":
    main(args=None)
