#! /usr/bin/python3

from game_class import BeloteGame
from player_class import Player, Dumb_Player

def main():
    game = BeloteGame([Dumb_Player("Alice"), Dumb_Player("Bob"), Dumb_Player("Charlie"), Dumb_Player("David")])
    game.play()

if __name__ == "__main__":
    main()