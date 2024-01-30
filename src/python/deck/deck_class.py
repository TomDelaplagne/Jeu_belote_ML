import random

from src.python.card.card_class import Card
from src.python.utils.constants import Suit, Rank

class Deck:
    """A class to represent a deck of cards."""
    def __init__(self, shuffle: bool = False, src: str = None):
        """Initialize the deck of cards.

        Args:
            src (str):  The source of the deck to copy. 
                        Defaults to None means that we rebuild the deck from scratch.
            shuffle (bool): Whether to shuffle the deck after building it. Defaults to False.
        """
        self.cards : list[Card] = []
        if src is None:
            for suit in Suit:
                for rank in Rank:
                    self.cards.append(Card(suit.value, rank.value))
            if shuffle:
                self.shuffle()
        else:
            if isinstance(src, Deck):
                self.cards = src.cards.copy()
            else:
                raise ValueError("Invalid source deck provided.")

    def shuffle(self, seed: int = None) -> None:
        """Shuffle the deck of cards in place.

        Args:
            seed (int): Optional random seed for reproducibility.
        """
        random.seed(seed)
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> list[Card]:
        """Deal a number of cards from the deck.

        Args:
            num_cards (int): The number of cards to deal.

        Returns:
            List[Card]: A list of dealt cards.
        """
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck.")
        return [self.cards.pop() for _ in range(num_cards)]

    def __repr__(self):
        return ", ".join([str(card) for card in self.cards])
