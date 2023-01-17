class Card:
    suits = ["trefles",
             "coeurs",
             "piques",
             "carreaux"]
    
    values = [None, None, "7",
              "8", "9", "10",
              "J", "Q",
              "K", "A"]

    def __init__(self, v, s):
        """suit + value are ints"""
        self.value = v
        self.suit = s

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        if self.value == c2.value:
            if self.suit < c2.suit:
                return True
            else:
                return False
        return False

    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        if self.value == c2.value:
            if self.suit > c2.suit:
                return True
            else:
                return False
        return False

    def __repr__(self):
        if self.suit%2 == 0:
            v = '\033[40m' + self.values[self.value] +\
                " de " + \
                self.suits[self.suit] + '\033[49m'
        elif self.suit%2 == 1:
            v = '\033[41m' + self.values[self.value] +\
                " de " + \
                self.suits[self.suit] + '\033[49m'

        return v