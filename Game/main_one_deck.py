#! /usr/bin/python3
"""This is the main routine for playing with 3 friends"""

from game_class import BeloteGame
from player_class import Player
from player_neural_class import Player_Neural

def main(args=None):
    """The main routine for playing with 3 friends"""
    Game = BeloteGame(Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4"))
    Game.play()
    

if __name__ == "__main__":
    main(args=None)