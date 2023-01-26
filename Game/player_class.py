from card_class import Card
from deck_class import PileOfCard

class Player:
    def __init__(self, name : str, teammate=None):
        self.name = name
        self.hand : PileOfCard
        self.tricks_taken = []
        self.teammate = teammate
        self.trump_suit = None

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
            except ValueError:
                print("Invalid card. Try again.")
                continue
            if (card not in hand):
                print("You don't have that card in your hand. Try again.")
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid):
        print(f"{self}, it is your turn to bid or pass. Your hand is: {self.hand}")
        bid = None
        while bid not in range(higgest_bid+10, 180, 10):
            print(f"Enter your bid between {higgest_bid+10} and 180 or 'CAPOT', press 'p' to pass:")
            bid = input()
            if bid == "p":
                print("You have passed.")
                return None
            if bid == "CAPOT":
                return 250
            try:
                bid = int(bid)
            except ValueError:
                print("Invalid bid. Try again.")
                continue
        return bid

    def take_trick(self, trick):
        self.tricks_taken.append(trick)


class Dumb_Player(Player):
    def __init__(self, name : str, teammate=None):
        super().__init__(name, teammate)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return super().__repr__() + " (Dumb)"

    def play_card(self, hand, msg):
        print(msg)
        # card = max(hand)
        card = hand[0]
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid):
        if higgest_bid == 70:
            return 80
        else:
            return None


class Smart_Player(Player):
    """A player that plays the best card in its hand."""

    def __init__(self, name : str, teammate=None):
        super().__init__(name, teammate)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return super().__repr__() + " (Smart)"

    def play_card(self, hand, msg):
        print(msg)
        card = self.maxCard(hand, self.trump_suit)
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid):
        if higgest_bid == 70:
            return 80
        else:
            return None

    def maxCard(self, hand, trump_suit):
        """Return the card with the highest value in the hand."""
        max_card = hand[0]
        for card in hand:
            if card.calculate_card_points(trump_suit) > max_card.calculate_card_points(trump_suit):
                max_card = card
        return max_card