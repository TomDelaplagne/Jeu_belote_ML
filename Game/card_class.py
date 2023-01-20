class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def calculate_card_points(self, trump_suit):
        """Calculate the points scored by a single card in the Belote game."""
        non_trump = {"Ace": 11, "10": 10, "King": 4, "Queen": 3, "Jack": 2, "9": 0, "8": 0, "7": 0}
        trump = {"Jack": 20, "9": 14, "Ace": 11, "10": 10, "King": 4, "Queen": 3, "8": 0, "7": 0}
        if self.suit == trump_suit:
            return trump[self.rank]
        else:
            return non_trump[self.rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, p2): # p1 == p2
        if p2 is None:
            return False
        return self.suit == p2.suit and self.rank == p2.rank