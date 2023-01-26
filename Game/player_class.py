"""This module contains the Player class and its subclasses."""

from card_class import Card

from deck_class import PileOfCard


class Player:
    """A class representing a player in the Belote game.

    Attributes:
    name (str): The name of the player.
    hand (PileOfCard): The cards in the player's hand.
    tricks_taken (list): The tricks taken by the player.
    teammate (Player): The player's teammate.
    trump_suit (str): The trump suit.

    Methods:
    declare_trump: Declare the trump suit.
    add_teammate: Add a teammate to the player.
    play_card: Play a card from the player's hand.
    """

    def __init__(self, name: str, teammate=None):
        """Initialize a player.

        Parameters:
        name (str): The name of the player.
        teammate (Player): The player's teammate.
        """
        self.name = name
        self.init_hand: PileOfCard
        self.hand: PileOfCard
        self.tricks_taken = []
        self.teammate = teammate
        self.trump_suit = None

    def declare_trump(self, trump_suit: str) -> None:
        """Declare the trump suit.

        Parameters:
        trump_suit (str): The trump suit.

        Returns:
        None
        """
        self.trump_suit = trump_suit

    def add_teammate(self, teammate: 'Player') -> None:
        """Add a teammate to the player.

        Parameters:
        teammate (Player): The player's teammate.

        Returns:
        None
        """
        self.teammate = teammate

    def __repr__(self):
        """Return a string representation of the player."""
        return self.name

    def __eq__(self, p2):
        """Return True if the players have the same name."""
        return self.name == p2.name

    def play_card(self, hand: PileOfCard, msg: str = '') -> Card:
        """Play a card from the player's hand.

        Parameters:
        hand (PileOfCard): The cards in the player's hand playable.
        msg (str): A message to display to the player.

        Returns:
        Card: The card played by the player.
        """
        print(f'{self.name}, it is your turn to play a card. Your hand is: \
            {hand}')
        print(msg)
        print("Enter the rank and suit of the card you want to play (e.g. \
            'Queen of Spades'):")

        card: Card = None
        while card is None or card not in hand:
            played_card = input()
            try:
                card = Card(*played_card.split(' of ')[::-1])
            except ValueError:
                print('Invalid card. Try again.')
                continue
            if (card not in hand):
                print("You don't have that card in your hand. Try again.")
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid: int) -> int:
        """Bid a number of points.

        Parameters:
        higgest_bid (int): The highest bid so far.

        Returns:
        int: The number of points bid by the player.
        """
        print(f'{self}, it is your turn to bid or pass. Your hand is: \
            {self.hand}')
        bid = None
        while bid not in range(higgest_bid+10, 180, 10):
            print(f"Enter your bid between {higgest_bid+10} and 180 \
                or 'CAPOT', press 'p' to pass:")
            bid = input()
            if bid == 'p':
                print('You have passed.')
                return None
            if bid == 'CAPOT':
                return 250
            try:
                bid = int(bid)
            except ValueError:
                print('Invalid bid. Try again.')
                continue
        return bid

    def take_trick(self, trick: PileOfCard) -> None:
        """Add a trick to the player's tricks_taken.

        Parameters:
        trick (list): The trick taken by the player.

        Returns:
        None
        """
        self.tricks_taken.append(trick)

    def belote(self) -> bool:
        """Return True if the player has a belote, False otherwise."""
        if 'King' in [
            card.rank for card in self.init_hand if self.is_trump(card)
            ] and 'Queen' in [
                card.rank for card in self.init_hand if self.is_trump(card)]:
            return True
        else:
            return False


class Dumb_Player(Player):
    """A player that plays the first card in its hand."""

    def __init__(self, name: str, teammate: Player = None):
        """Initialize a dumb player.

        Parameters:
        name (str): The name of the player.
        teammate (Player): The player's teammate.
        """
        super().__init__(name, teammate)

    def __hash__(self) -> str:
        """Return the hash of the player's name."""
        return hash(self.name)

    def __repr__(self) -> str:
        """Return a string representation of the player."""
        return super().__repr__() + ' (Dumb)'

    def play_card(self, hand: PileOfCard, msg: str) -> Card:
        """Play a card from the player's hand.

        Parameters:
        hand (PileOfCard): The cards in the player's hand playable.
        msg (str): A message to display to the player.

        Returns:
        Card: The card played by the player.
        """
        print(msg)
        # card = max(hand)
        card = hand[0]
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid: int) -> int:
        """Bid a number of points.

        Parameters:
        higgest_bid (int): The highest bid so far.

        Returns:
        int: The number of points bid by the player.
        """
        if higgest_bid == 70:
            return 80
        else:
            return None


class Smart_Player(Player):
    """A player that plays the best card in its hand.

    Methods:
    maxCard: Return the best card in a list of cards.
    """

    def __init__(self, name: str, teammate=None):
        """Initialize a smart player.

        Parameters:
        name (str): The name of the player.
        teammate (Player): The player's teammate.
        """
        super().__init__(name, teammate)

    def __repr__(self):
        """Return a string representation of the player."""
        return super().__repr__() + ' (Smart)'

    def play_card(self, hand: PileOfCard, msg: str) -> Card:
        """Play a card from the player's hand.

        Parameters:
        hand (PileOfCard): The cards in the player's hand playable.
        msg (str): A message to display to the player.

        Returns:
        Card: The card played by the player.
        """
        print(msg)
        card = self.maxCard(hand, self.trump_suit)
        self.hand.remove(card)
        return card

    def bid(self, higgest_bid: int) -> int:
        """Bid a number of points.

        Parameters:
        higgest_bid (int): The highest bid so far.

        Returns:
        int: The number of points bid by the player.
        """
        if higgest_bid == 70:
            return 80
        else:
            return None

    def maxCard(self, hand, trump_suit):
        """Return the card with the highest value in the hand."""
        max_card = hand[0]
        for card in hand:
            if (card.calculate_card_points(trump_suit)
                    > max_card.calculate_card_points(trump_suit)):
                max_card = card
        return max_card
