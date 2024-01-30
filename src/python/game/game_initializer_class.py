"""This module contains the GameInitializer class."""

class GameInitializer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameInitializer, cls).__new__(cls)
        return cls._instance

    def initialize_game(self, players, deck):
        # ... logic for dealing cards, determining trump suit, etc.

    def play_game(self, players, current_trick, played_cards, trump_suit):
        # ... logic for playing tricks, determining trick winner, etc.
