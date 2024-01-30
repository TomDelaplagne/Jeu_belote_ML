#! /usr/bin/python3
"""This is the main routine for playing with 3 friends"""

from src.python.game.game_class import Game
# from src.python.player.player_class import HumanPlayer
from src.python.player.player_class import DumbPlayer


def main(args=None):
    """The main routine for playing with 3 friends"""
    game = Game(DumbPlayer("Player1"),
                DumbPlayer("Player2"),
                DumbPlayer("Player3"),
                DumbPlayer("Player4"))
    game.play()

if __name__ == "__main__":
    main(args=None)
