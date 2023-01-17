class Card:
    suits = ["trefles",
             "coeurs",
             "carreaux",
             "piques"]
    
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
        v = self.values[self.value] +\
            " de " + \
            self.suits[self.suit]
        return v