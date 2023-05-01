""""""
from player_class import Player

class QPlayer(Player):
    """A player that use a Q-learning algorithm to play."""
    def __init__(self, name):
        super().__init__(name)
        self.action: int = None

    def play_card(self, msg):
        """Play a card."""
        if self.action is None:
            raise ValueError("The action must be set before playing a card.")
        card = self.hand[self.action]
        self.hand.remove(card)
        self.action = None
        return card

    def __repr__(self):
        return super().__repr__() + " (Q)"