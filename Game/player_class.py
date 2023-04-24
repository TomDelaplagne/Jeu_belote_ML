from copy import deepcopy
from typing import TypeVar

from card_class import Card
from deck_class import PileOfCard
from dataclasses import dataclass, field
from bid_class import Bid

PileOfCardType = TypeVar("PileOfCardType", bound="PileOfCard")

@dataclass(repr=False, slots=True)
class Player:
    name: str
    teammate: "Player" = field(default=None)
    hand: PileOfCardType = field(default_factory=PileOfCard)
    hand_at_beginning: PileOfCardType = field(default_factory=PileOfCard)
    tricks_taken: list[tuple] = field(repr=False, default_factory=list)
    trump_suit: str = field(default=None, repr=False)

    def __post_init__(self):
        self.hand_at_beginning = self.hand.copy()

    def declare_trump(self, trump_suit):
        self.trump_suit = trump_suit
    
    def add_teammate(self, teammate):
        self.teammate = teammate

    def __repr__(self):
        return self.name

    def __eq__(self, p2):
        return self.name == p2.name

    def play_card(self, hand, msg):
        print(f"{self.name}, it is your turn to play a card. Your hand is: {hand}")
        print(msg)
        print("Enter the rank and suit of the card you want to play (e.g. 'Queen of Spades'):")
        
        card : Card = None
        while card == None or card not in hand:
            played_card = input()
            try :
                card = Card(*played_card.split(" of ")[::-1])
            except :
                print("Invalid card. Try again.")
                continue
            if (card not in hand):
                print("You don't have that card in your hand. Try again.")
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid: Bid):
        print(f"{self}, it is your turn to bid or pass. Your hand is: {self.hand}")
        bid = None
        higgest_bid_amount = higgest_bid.bid
        while bid not in range(higgest_bid_amount+10, 180, 10):
            print(f"Enter your bid between {higgest_bid_amount+10} and 180 or 'CAPOT', press 'p' to pass:")
            bid = input()
            if bid == "p":
                print("You have passed.")
                return None
            print(f'You entered {bid}, which trump suit do you want? (Spades, Hearts, Diamonds, Clubs)')
            trump = input()
            if trump not in ["Spades", "Hearts", "Diamonds", "Clubs"]:
                print("Invalid trump suit. Try again.")
                continue
            if bid == "CAPOT":
                return Bid(self, 250, trump)
            try:
                bid = int(bid)
            except ValueError:
                print("Invalid bid. Try again.")
                continue
        return Bid(self, bid, trump)

    def take_trick(self, trick):
        self.tricks_taken.append(trick)

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "teammate": self.teammate.name if self.teammate else None,
            "hand": self.hand,
            "tricks_taken": [trick[0].get_dict() for trick in self.tricks_taken],
            "trump_suit": self.trump_suit
        }
    
    def __hash__(self):
        return hash(self.name)

class Dumb_Player(Player):
    """A player that plays the first card in its hand"""
    def __init__(self, name : str, teammate=None):
        super().__init__(name, teammate)

    def __repr__(self):
        return super().__repr__() + " (Dumb)"

    def play_card(self, hand, msg):
        print(msg)
        card = hand[0]
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid: Bid):
        higgest_bid_amount = higgest_bid.bid
        if higgest_bid_amount == 70:
            return Bid(self, 80, "Spades")
        else:
            return None
