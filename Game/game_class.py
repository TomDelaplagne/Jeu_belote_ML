"""A module containing the BeloteGame class."""

from copy import deepcopy

from player_class import Player
from deck_class import Deck

class BeloteGame:
    """A class to represent a game of Belote."""
    def __init__(self, *players: list[Player], deck = None):
        self.players: list[Player] = players
        self.deck: Deck = deck if deck else None
        self.trump_suit = "Hearts"
        self.current_trick = []
        self.played_cards = []

        # Shuffle and deal cards
        if self.deck is None:
            self.deck = Deck()
            self.deck.shuffle()

        hands = [self.deck.deal(2) for _ in self.players]
        for i, hand in enumerate(hands):
            self.players[i].hand = hand

    def play(self):
        """Shuffles and deals cards, starts bidding, plays tricks, calculates points, and prints results."""

        # Play the tricks
        trick_winner : Player = None
        for _ in range(2):
            trick_winner = self.play_trick(trick_winner)

        # Calculate and assign points
        points = self.calculate_points()

        return points

    def play_trick(self, trick_winner=None):
        """Play a trick of the game."""

        if trick_winner is None:
            # This is the first trick of the game, so the player 1 is the first player
            indx_current_player = 0
        else:
            # The winner of the previous trick is the first player
            indx_current_player = self.players.index(trick_winner)

        self.current_trick = []
        led_suit = None
        for player in self.players[indx_current_player:] + self.players[:indx_current_player]:
            card = player.play_card(f"{player} can play any card")
            if led_suit is None:
                led_suit = card.suit
            trick_winner = player
            self.current_trick.append(deepcopy(card))
            self.played_cards.append(deepcopy(card))

        trick_winner = self.determine_trick_winner(self.current_trick, led_suit)

        self.players[self.players.index(trick_winner)].tricks_taken.append(deepcopy(self.current_trick))
        return trick_winner

    def determine_trick_winner(self, trick, led_suit):
        """Determine the winner of a trick."""
        if any("Hearts" in card.suit for card in trick):
            # There is at least one trump card in the trick
            trick_winner_card = max([card for card in trick if card.suit == self.trump_suit], key=lambda card: card.rank)
            trick_winner = self.players[trick.index(trick_winner_card)]
            return trick_winner
        elif any(led_suit in card.suit for card in trick):
            # There is at least one card of the led suit in the trick but no trump card
            trick_winner_card = max([card for card in trick if card.suit == led_suit], key=lambda card: card.rank)
            trick_winner = self.players[trick.index(trick_winner_card)]
            return trick_winner
        else:
            raise ValueError("There is no card of the led suit in the trick")
            # There is no card of the led suit in the trick
            # trick_winner_card = max(trick, key=lambda card: card.rank)
            # trick_winner = self.players[trick.index(trick_winner_card)]
            # return trick_winner

    def is_trump(self, card):
        """Return True if the card is a trump card, False otherwise."""
        return card.suit == self.trump_suit

    def calculate_points(self):
        """Calculate the points scored by each team in the current hand."""
        points = {player: 0 for player in self.players}
        # Calculate tricks_taken points
        for player in self.players:
            for trick in player.tricks_taken:
                for card in trick:
                    points[player] += card.calculate_card_points()
        points = {player: round(points[player], -1) for player in self.players}
        return points
