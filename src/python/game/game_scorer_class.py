"""This module contains the GameScorer class."""

from src.python.card.card_class import Card
from src.python.player.player_class import Player
from src.python.utils.constants import Suit

class GameScorer:
    def __init__(self, players: list[Player], trump_suit: Suit):
        """Initialize a GameScorer instance.

        Args:
            players (list[Player]): The players of the game, they are observers of the game scorer.
        """
        self.players: list[Player] = players
        self.trump_suit: Suit = trump_suit
        self.game_total_points: int = 0
        self.teams: list[list[Player]] = [[self.players[0], self.players[2]],
                                          [self.players[1], self.players[3]]]

    def totalize_points(self) -> dict[list[Player]: int]:
        """Calculate the points scored by each team at the end of the game."""

        team_points = {}
        for team in self.teams:
            points = self.calculate_team_points(team)

            team_points[team] = points
        return team_points

    def calculate_trick_points(self, trick: list[Card]) -> int:
        """Calculate the points scored trick."""
        return sum(card.calculate_card_points(self.trump_suit) for card in trick)

    def calculate_player_points(self, player: Player) -> int:
        """Calculate the belote points scored by a player."""
        # Add 20 points if the player has the belote (i.e. the king and queen of the trump suit).
        player_points = sum(card.calculate_card_points(self.trump_suit) for card in player.tricks)
        if player.has_belote(self.trump_suit):
            player_points += 20
        return player_points

    def calculate_team_points(self, team: list[Player]) -> int:
        """Calculate the points scored by a team."""
        return sum(self.calculate_player_points(player) for player in team)
