from card_class import Card
from player_class import Player
import numpy as np
from bid_class import Bid
import json

class Player_Neural(Player):
    def __init__(self, name : str, teammate=None):
        super().__init__(name, teammate)
        self.strategy = None

    def play_card(self, hand, msg):
        card = hand[0]
        self.hand.remove(card)
        return card

    def bid(self, highest_bid: Bid) -> Bid or None:
        if highest_bid.bid <= 100 or highest_bid is None:
            # Lancelot prend à 110 si il a au moins un des cas suivants:
            # V9xx + 2 As ou A-10
            # V9A + 3 As / V9A + 1 As + A-10
            suit = self.in_hand("V", "9", "x", "x")
            if suit and self.count_as_in_hand() >= 2:
                return Bid(self, 110, suit)
            suit_AS_10 = self.in_hand("A", "10")
            if suit_AS_10 and suit and suit != suit_AS_10:
                return Bid(self, 110, suit)
            suit = self.in_hand("V", "9", "A")
            if suit and self.count_as_in_hand() >= 3:
                return Bid(self, 110, suit)

        if highest_bid.bid <= 90 or highest_bid is None:
            # Lancelot prend à 100 si il a au moins un des cas suivants:
            # V9xx + 1 As ou 10xx
            # V9A + 2 As ou A-10
            suit = self.in_hand("V", "9", "x", "x")
            if suit and self.count_as_in_hand() >= 1:
                return Bid(self, 100, suit)
            suit_AS_10 = self.in_hand("10","x","x")
            if suit_AS_10 and suit and suit != suit_AS_10:
                return Bid(self, 100, suit)
            suit = self.in_hand("V", "9", "A")
            if suit and self.count_as_in_hand() >= 2:
                return Bid(self, 100, suit)
            suit_AS_10 = self.in_hand("A", "10")
            if suit_AS_10 and suit and suit != suit_AS_10:
                return Bid(self, 100, suit)

        if highest_bid.bid <= 80 or highest_bid.bid is None:
            # Lancelot prend à 80 si il a au moins un des cas suivants:
            # V9xx
            # V9x + 1 As
            # V9 + 2 As ou A-10
            suit = self.in_hand("V", "9", "x", "x")
            if suit:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "9", "x")
            if suit and self.count_as_in_hand() >= 1:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "9")
            if suit and self.count_as_in_hand() >= 2:
                return Bid(self, 80, suit)
            suit_AS_10 = self.in_hand("A", "10")
            if suit_AS_10 and suit and suit != suit_AS_10:
                return Bid(self, 80, suit)

        if highest_bid is None:
            # Lancelot fait une offre de 80 si il a au moins un des cas suivants:
            # 9RDx ou Vxxx ou 9xxx + 1 As
            # V9x ou VA10 ou VRD
            # Vxx + 1 As ou 9xx + 2 As ou AS-10
            # Vx + 2 As ou V9 + 1 As
            suit = self.in_hand("9", "R", "D", "x")
            if suit:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "x", "x", "x")
            if suit:
                return Bid(self, 80, suit)
            suit = self.in_hand("9", "x", "x", "x")
            if suit and self.count_as_in_hand() >= 1:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "9", "x")
            if suit:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "A", "10")
            if suit:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "R", "D")
            if suit:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "x", "x")
            if suit and self.count_as_in_hand() >= 1:
                return Bid(self, 80, suit)
            suit = self.in_hand("9", "x", "x")
            if suit and self.count_as_in_hand() >= 2:
                return Bid(self, 80, suit)
            suit_AS_10 = self.in_hand("A", "10")
            if suit_AS_10 and suit and suit != suit_AS_10:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "x")
            if suit and self.count_as_in_hand() >= 2:
                return Bid(self, 80, suit)
            suit = self.in_hand("V", "9")
            if suit and self.count_as_in_hand() >= 1:
                return Bid(self, 80, suit)
        
        # Lancelot ne peut pas faire d'offre plus élevée
        return None

    def in_hand(self, *args):
        assert len(args) > 0
        hand_rank = [card.rank for card in self.hand]
        hand_suit = [card.suit for card in self.hand]
        for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            suit_cards = []
            for i, rank in enumerate(args):
                if rank in hand_rank and hand_suit[i] == suit:
                    suit_cards.append(rank)
                if rank == "x" and rank not in hand_rank and hand_suit[i] == suit:
                    suit_cards.append(rank)
            if len(suit_cards) == len(args):
                return suit
        return False

    def count_as_in_hand(self):
        # compter le nombre d'As dans la main de Lancelot
        return sum(1 for card in self.hand if card.rank == 'A')

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "teammate": self.teammate.name if self.teammate else None,
            "hand": self.hand,
            "tricks_taken": [trick[0].get_dict() for trick in self.tricks_taken],
            "trump_suit": self.trump_suit
        }
    
    # def __del__(self):
    #     print(f"{self} est mort")