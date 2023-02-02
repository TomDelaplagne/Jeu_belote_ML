class Bid:
    def __init__(self, player: "Player", bid: int, trump: str):
        self.player: Player = player
        self.bid: int = bid
        self.trump: str = trump # Spades, Hearts, Diamonds, Clubs