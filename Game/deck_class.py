"""This module contains the Deck class and PileOfCard."""

import random

from card_class import Card


class PileOfCard(list):
    """A class representing a pile of cards.

    This class inherits from the list class and has a method for calculating
    the points scored by the pile of cards.

    Attributes:
    None

    Methods:
    calculate_points: Calculate the points scored by the pile of cards.
    """

    def __init__(self, *args: Card):
        """Initialize a pile of cards.

        Parameters:
        args (Card): The cards in the pile.
        """
        super().__init__(arg for arg in args if type(arg) == Card)

    def append(self, __item: Card) -> 'PileOfCard':
        """Append a card to the pile.

        Parameters:
        __item (Card): The card to append.

        Returns:
        PileOfCard: The pile of cards.
        """
        super().append(__item)
        return self

    def pop(self, index=-1):
        return super().pop(index)

    def calculate_points(self, trump_suit):
        return sum([card.calculate_card_points(trump_suit) for card in self])

    def __repr__(self):
        """Return a string representation of the pile of cards.

        Returns:
        str: The string representation of the pile of cards.
        """
        return ', '.join([str(card) for card in self])


    def load_deck(self, src):
        with open(src, "r") as f:
            for line in f:
                self.append(Card(*(line.strip()).split(" of ")[::-1]))

    def save_deck(self, src):
        with open(src, "w") as f:
            for card in self:
                f.write(str(card) + "\n")

    def get_dict(self) -> dict:
        return [card.get_dict() for card in self]

class Deck():
    def __init__(self, src: str = None):
        self.cards : PileOfCard = PileOfCard()
        if src is None:
            for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
                for rank in ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7"]:
                    self.cards.append(Card(suit, rank))
        else:
            self.cards.load_deck(src)

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return PileOfCard(*[self.cards.pop() for _ in range(num_cards)])

    def __repr__(self):
        return ", ".join([str(card) for card in self.cards])

    def save_deck(self, src):
        self.cards.save_deck(src)
    
    def load_deck(self, src):
        self.cards.load_deck(src)

    def get_dict(self) -> dict:
        return self.cards.get_dict()
