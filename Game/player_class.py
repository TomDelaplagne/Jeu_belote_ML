"""A module containing the Player class and the DumbPlayer class."""
from dataclasses import dataclass, field

from card_class import Card


@dataclass(repr=False, slots=True)
class Player:
    """A class to represent a single player in the Belote game."""
    name: str
    teammate: "Player" = field(default=None)
    hand: list = field(default_factory=list)
    tricks_taken: list[tuple] = field(repr=False, default_factory=list)
    trump_suit: str = field(default="Hearts", repr=False)

    def __repr__(self):
        return self.name

    def __eq__(self, player_2):
        return self.name == player_2.name

    def play_card(self, msg):
        """Play a card from the player's hand."""
        print(f"{self.name}, it is your turn to play a card. Your hand is: {self.hand}")
        print(msg)
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
        self.hand.remove(card)
        return card

    def take_trick(self, trick):
        """Add a trick to the player's list of tricks taken."""
        self.tricks_taken.append(trick)

    def get_dict(self) -> dict:
        """Return a dictionary representation of the player."""
        return {
            "name": self.name,
            "teammate": self.teammate.name if self.teammate else None,
            "hand": self.hand,
            "tricks_taken": [trick[0].get_dict() for trick in self.tricks_taken],
            "trump_suit": self.trump_suit
        }

    def __hash__(self):
        return hash(self.name)


class DumbPlayer(Player):
    """A player that plays the first card in its hand"""
    def __init__(self, name : str, teammate=None):
        super().__init__(name, teammate)

    def __repr__(self):
        return super().__repr__() + " (Dumb)"

    def play_card(self, msg):
        """Play the first card in the hand."""
        card = self.hand[0]
        self.hand.remove(card)
        return card
