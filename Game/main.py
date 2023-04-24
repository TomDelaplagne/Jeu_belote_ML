"""module to train the neural network on one deck"""

import os
from contextlib import redirect_stdout

import torch
from torch import nn

import matplotlib.pyplot as plt

from game_class import BeloteGame
from player_class import Dumb_Player
from player_neural_class import PlayerNeural


def init_weights(model):
    """Initialize the weights of the neural network"""
    if isinstance(model, nn.Linear):
        torch.nn.init.xavier_uniform_(model.weight.data)
        model.bias.data.fill_(0.01)

def create_model(input_size=32, output_size=8, hidden_size=(16, 16)):
    """Create a neural network model with 2 hidden layers"""
    model = nn.Sequential(
        nn.Linear(input_size, hidden_size[0]),
        nn.ReLU(),
        nn.Linear(hidden_size[0], hidden_size[1]),
        nn.ReLU(),
        nn.Linear(hidden_size[1], output_size)
    )

    torch.manual_seed(0)
    model.apply(init_weights)
    return model

def main():
    """Train the neural network by playing against dumb players"""

    # first create the neural network model and the neural player
    model = create_model()
    neural_player = PlayerNeural("NeuralPlayer", model)

    # then create the game
    Game = BeloteGame(neural_player, Dumb_Player("Player2"), Dumb_Player("Player3"), Dumb_Player("Player4"))

    loss_fn = nn.MSELoss()

    nb_epoch = 50

    optimizer = torch.optim.SGD(neural_player.model.parameters(), lr=0.1)

    loss_over_epoch = []

    for _ in range(nb_epoch):
        with redirect_stdout(open(os.devnull, "w", encoding="utf-8")):
            points = Game.play()[str(neural_player)]
        max_points = 320.0
        l = loss_fn(torch.tensor(points), torch.tensor(max_points))
        optimizer.zero_grad()
        l.backward()
        optimizer.step()
        loss_over_epoch.append(l.item())
        print(f"Loss: {l.item()}")


    print(f"Final loss: {loss_over_epoch[-1]}")

    # save the model
    torch.save(neural_player.model.state_dict(), "model.pth")

    plt.figure()
    plt.plot(loss_over_epoch)
    plt.title("Loss over epoch")
    plt.xlabel('epoch'), plt.ylabel('loss')
    plt.show()

if __name__ == "__main__":
    main()
