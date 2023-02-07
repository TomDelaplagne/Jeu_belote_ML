from dataclasses import dataclass

@dataclass(frozen=True, eq=True, slots=True, repr=False) # frozen=True: immutable
class Card:
    """A class to represent a single card in the Belote game."""
    suit: str # Spades, Hearts, Diamonds, Clubs
    rank: str # Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King


    def points(self, trump_suit: str) -> int:
        """
        Calculate the points scored by a single card in the Belote game.

        Parameters:
        trump_suit (str): the trump suit

        Returns:
        int: the points scored by the card.
        """
        non_trump = {
            'Ace': 11,
            '10': 10,
            'King': 4,
            'Queen': 3,
            'Jack': 2,
            '9': 0,
            '8': 0,
            '7': 0
            }
        trump = {
            'Jack': 20,
            '9': 14,
            'Ace': 11,
            '10': 10,
            'King': 4,
            'Queen': 3,
            '8': 0,
            '7': 0
            }
        if self.suit == trump_suit:
            return trump[self.rank]
        else:
            return non_trump[self.rank]

    def __repr__(self) -> str:
        """Return a string representation of a card."""
        return f'{self.rank} of {self.suit}'


    def get_dict(self) -> dict:
        return {"suit": self.suit, "rank": self.rank}

    def __eq__(self, p2) -> bool:
        """Return True if two cards are equal."""
        if p2 is None:
            return False
        return self.suit == p2.suit and self.rank == p2.rank

