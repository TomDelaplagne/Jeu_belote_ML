from random import shuffle
from card_class import Card

class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 10):
            for j in range(4):
                self.cards\
                    .append(Card(i,
                                 j))
        shuffle(self.cards)

    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()