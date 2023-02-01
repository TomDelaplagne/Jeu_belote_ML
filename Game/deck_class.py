import random
from card_class import Card

class PileOfCard(list):
    def __init__(self, *args):
        super().__init__(arg for arg in args if type(arg) == Card)

    def append(self, __item : Card):
        super().append(__item)
        return self

    def pop(self, index=-1):
        return super().pop(index)

    def calculate_points(self, trump_suit):
        return sum([card.calculate_card_points(trump_suit) for card in self])

    def __repr__(self):
        return ", ".join([str(card) for card in self])

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