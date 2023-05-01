import random
from card_class import Card

class Deck():
    """A class to represent a deck of cards."""
    def __init__(self, src: str = None):
        self.cards : list = []
        if src is None:
            for suit in ["Spades", "Hearts", "Diamonds"]:
                for rank in [1, 2]:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def deal(self, num_cards):
        """Deal a number of cards from the deck."""
        return [self.cards.pop() for _ in range(num_cards)]

    def __repr__(self):
        return ", ".join([str(card) for card in self.cards])
