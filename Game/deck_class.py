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

    def calculate_points(self, trump_suit: str) -> int:
        """Calculate the points scored by the pile of cards.

        Parameters:
        trump_suit (str): The trump suit.

        Returns:
        int: The points scored by the pile of cards.
        """
        return sum([card.calculate_card_points(trump_suit) for card in self])

    def __repr__(self):
        """Return a string representation of the pile of cards.

        Returns:
        str: The string representation of the pile of cards.
        """
        return ', '.join([str(card) for card in self])


class Deck():
    """A class representing a deck of cards.

    This class has methods for shuffling and dealing cards.

    Attributes:
    cards (PileOfCard): The cards in the deck.

    Methods:
    shuffle: Shuffle the deck of cards.
    deal: Deal a number of cards from the deck.
    """

    def __init__(self):
        """Initialize a deck of cards.

        The deck is initialized with 32 cards, 8 cards for each suit.
        """
        self.cards: PileOfCard = []
        for suit in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            for rank in ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7']:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> list:
        """Deal a number of cards from the deck.

        Parameters:
        num_cards (int): The number of cards to deal.

        Returns:
        list: The list of cards dealt.
        """
        return [self.cards.pop() for _ in range(num_cards)]
