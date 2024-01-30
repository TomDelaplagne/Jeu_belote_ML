"""File for storing constants that are used throughout the game."""

from enum import Enum

class Suit(Enum):
    """An enumeration of the suits of the cards in the game."""
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"

class Rank(Enum):
    """An enumeration of the ranks of the cards in the game."""
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    ACE = "Ace"

# trump_card_points & card_points are enumerate of (rank, points) tuples
CARD_POINTS = [0, 0, 0, 0, 10, 2, 3, 4, 11]
TRUMP_CARD_POINTS = [0, 0, 14, 10, 20, 3, 4, 11]

# rank_to_points is a dictionary mapping ranks to points
RANK_TO_POINTS = {rank: points for rank, points in zip(Rank, CARD_POINTS)}

# rank_to_trump_points is a dictionary mapping ranks to trump points
RANK_TO_TRUMP_POINTS = {rank: points for rank, points in zip(Rank, TRUMP_CARD_POINTS)}

# nb_cards_per_player is the number of cards each player gets at the start of the game
NB_CARDS_PER_PLAYER = 8
