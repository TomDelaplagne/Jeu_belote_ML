"""This file contains the abstract class for the strategy pattern."""

from abc import ABC, abstractmethod

from src.python.card.card_class import Card
from src.python.utils.constants import Suit

class Strategy(ABC):
    """A class to represent a strategy for playing a card from a player's hand."""
    def __init__(self, player_name : str):
        self.player_name = player_name

    @abstractmethod
    def play_card(self, context_msg, hand, trick_cards, trump_suit) -> Card:
        """Play a card from the player's hand."""
        raise NotImplementedError

class HumanStrategy(Strategy):
    """A class to represent a human strategy for playing a card from a player's hand."""
    def play_card(self, context_msg, hand: list[Card], trick_cards: list[Card], trump_suit: Suit) -> Card:
        print(f"{self.player_name}, it is your turn to play a card. Your hand is: {hand}")
        print(context_msg)
        print("Enter the rank and suit of the card you want to play (e.g. 'Queen of Spades'):")

        card : Card = None
        while card is None or card not in hand:
            played_card = input()
            try :
                suit, rank = played_card.split(" of ")[::-1]
                rank = int(rank)
                card = Card(suit, rank)
            except ValueError:
                print("Invalid card. Try again.")
                continue
            if card not in hand:
                print("You don't have that card in your hand. Try again.")
        hand.remove(card)
        return card

