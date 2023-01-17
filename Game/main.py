#! /usr/bin/python3

from game_class import BeloteGame
from player_class import Player

def main():
    game = BeloteGame([Player("Alice"), Player("Bob"), Player("Charlie"), Player("David")])
    game.play()

if __name__ == "__main__":
    main()
