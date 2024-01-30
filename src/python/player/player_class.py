"""A module containing the Player class and the DumbPlayer class."""
from dataclasses import dataclass, field

from abc import ABC, abstractmethod

from src.python.card.card_class import Card
from src.python.utils.constants import Suit

@dataclass(repr=False, slots=True)
class Player(ABC):
    """A class to represent a single player in the Belote game."""
    name: str
    teammate: "Player" = field(default=None)
    hand: list = field(default_factory=list)
    tricks_taken: list[tuple] = field(repr=False, default_factory=list)

    def __repr__(self):
        return self.name

    def __eq__(self, player_2):
        return self.name == player_2.name

    def reset(self):
        """Reset the player's hand and tricks taken."""
        self.hand = []
        self.tricks_taken = []

    def play_card(self,
                  context_msg: str,
                  trick_cards: list[Card],
                  trump_suit: Suit) -> Card:
        """Play a card from the player's hand."""

        # check if strategy is not an abstract method
        if self.strategy == Player.strategy:
            raise ValueError("Player strategy is not set.")
        if len(self.hand) == 0:
            raise ValueError("Player has no cards in hand.")
        card = self.strategy(context_msg, trick_cards, trump_suit)
        self.hand.remove(card)
        return card

    @abstractmethod
    def strategy(self,
                 context_msg: str,
                 trick_cards: list[Card],
                 trump_suit: Suit)-> Card:
        """Play a card from the player's hand."""
        raise NotImplementedError

    def take_trick(self, trick: list[Card]):
        """Add a trick to the player's list of tricks taken."""
        self.tricks_taken.append(trick)

class HumanPlayer(Player):
    """A class to represent a single human player in the Belote game."""
    def __init__(self, name : str, teammate: Player=None):
        super().__init__(name, teammate)

    def strategy(self,
                 context_msg: str,
                 trick_cards: list[Card],
                 trump_suit: Suit):
        """Play a card from the player's hand."""
        print(f"{self.name}, it is your turn to play a card. Your hand is: {self.hand}")
        print(context_msg)
        print(f"The current trick is: {trick_cards}")
        print(f"The trump suit is: {trump_suit}")
        print("Enter the rank and suit of the card you want to play (e.g. 'Queen of Spades'):")

        card : Card = None
        while card is None or card not in self.hand:
            played_card = input()
            try :
                suit, rank = played_card.split(" of ")[::-1]
                rank = int(rank)
                card = Card(suit, rank)
            except ValueError:
                print("Invalid card. Try again.")
                continue
            if card not in self.hand:
                print("You don't have that card in your hand. Try again.")
        return card

class DumbPlayer(Player):
    """A player that plays the first card in its hand"""
    def __init__(self, name : str, teammate=None):
        super().__init__(name, teammate)

    def __repr__(self):
        return super().__repr__() + " (Dumb)"

    def play_card(self, _, __, ___):
        """Play the first card in the hand."""
        card = self.hand[0]
        self.hand.remove(card)
        return card
