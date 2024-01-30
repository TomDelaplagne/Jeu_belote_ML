#! /usr/bin/python3
"""This is the main routine for playing with 3 friends"""

from game_class import BeloteGame
from src.python.player.player_class import HumanPlayer

def main(args=None):
    """The main routine for playing with 3 friends"""
    game = BeloteGame(HumanPlayer("Player1"),
                      HumanPlayer("Player2"),
                      HumanPlayer("Player3"),
                      HumanPlayer("Player4"))
    game.play()

if __name__ == "__main__":
    main(args=None)
