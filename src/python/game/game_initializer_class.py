"""This module contains the GameInitializer class."""

from src.python.player.player_class import Player
from src.python.deck.deck_class import Deck

class GameInitializer:
    """This class initializes a game of Belote."""
    players: list[Player]
    shuffle: bool = True
    _instance = None
    deck: Deck = Deck(shuffle=shuffle)

    @classmethod
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameInitializer, cls).__new__(cls)
        return cls._instance

    def initialize_game(self, players):
        # ... logic for dealing cards, determining trump suit, etc.
        pass

    @staticmethod
    def set_partners(self, players):
        # ... logic for setting partners
        pass

    @staticmethod
    def deal_cards(self, players, deck):
        # ... logic for dealing cards
        pass