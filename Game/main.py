#! /usr/bin/python3

from game_class import Game
import os
import sys

def main():
    os.system('clear')
    first_game = Game()
    first_game.play_game()

if __name__ == '__main__':
    main()

