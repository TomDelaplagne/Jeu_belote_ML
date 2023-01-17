import random

from card_class import Card

class PileOfCard(list):
    def __init__(self, *args):
        super.__init__(*args)
        self = []

    def calculate_points(self, trump_suit):
        # TODO : this function then change the code from game_class to use this method
        return sum([card.calculate_card_points(trump_suit) for card in self])

    def __repr__(self):
        return ", ".join([str(card) for card in self])

class Deck():
    def __init__(self):
        self.cards : PileOfCard = []
        for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            for rank in ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7"]:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
    
