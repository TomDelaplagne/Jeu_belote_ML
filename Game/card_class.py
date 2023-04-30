from dataclasses import dataclass

@dataclass(frozen=True, eq=True, slots=True, repr=False) # frozen=True: immutable
class Card:
    """A class to represent a single card in the Belote game."""
    suit: str
    rank: int

    def calculate_card_points(self):
        """Calculate the points scored by a single card in the Belote game."""
        if self.suit == "Hearts":
            return self.rank*2
        else:
            return self.rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def get_dict(self) -> dict:
        return {"suit": self.suit, "rank": self.rank}
