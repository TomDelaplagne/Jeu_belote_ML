from dataclasses import dataclass

from src.python.utils.constants import RANK_TO_POINTS, RANK_TO_TRUMP_POINTS
from src.python.utils.constants import Suit
from src.python.utils.constants import Rank

@dataclass(frozen=True, eq=True, slots=True, repr=False) # frozen=True: immutable
class Card:
    """A class to represent a single card."""
    suit: Suit
    rank: Rank

    def calculate_card_points(self, trump_suit: Suit) -> int:
        """Calculate the points scored by a single card in the Belote game."""
        if self.suit == trump_suit:
            return RANK_TO_POINTS[self.rank]
        return RANK_TO_TRUMP_POINTS[self.rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
