"""This module contains the BeloteGame class."""

from typing import List, Tuple

from card_class import Card

from deck_class import Deck, PileOfCard

from player_class import Player


class BeloteGame:
    """A class representing a game of Belote.

    Attributes:
    players (list): The players in the game.
    deck (Deck): The deck of cards.
    trump_suit (str): The trump suit.

    Methods:
    play: Play the game.
    start_bidding: Start the bidding.
    play_trick: Play a trick.
    """

    def __init__(self, players: list[Player]):
        """Initialize a game of Belote.

        Parameters:
        players (list): The players in the game.
        """
        self.players = players
        for player in players:
            player.add_teammate(
                players[(players.index(player) + 2) % 4]
                )
        self.deck = Deck()
        self.trump_suit = None

    def play(self):
        """Shuffles and deals cards, starts bidding, plays tricks, calculates \
            points, and prints results."""
        # Shuffle and deal cards
        self.deck.shuffle()
        hands = [self.deck.deal(8) for _ in self.players]
        for i, hand in enumerate(hands):
            self.players[i].init_hand = hand[:]
            self.players[i].hand = hand[:]

        # Start the bidding
        (declarer, bid) = self.start_bidding()

        # declare_trump for players
        for player in self.players:
            player.declare_trump(self.trump_suit)

        try:
            type(declarer) == Player
        except NameError:
            # All players have passed, restart the game
            return

        # Declare the trump suit
        self.trump_suit = self.declare_trump(declarer)

        # Play the tricks
        trick_winner: Player = None
        for i in range(8):
            trick_winner = self.play_trick(i, trick_winner)

        # Calculate and assign points
        points = self.calculate_points()

        # Print the results
        self.print_results(points, bid, declarer)

    def start_bidding(self) -> Tuple[Player, int]:
        """Prompt each player to bid or pass until a bid is accepted or all \
            players pass."""
        print('Starting the bidding...')
        current_player: Player = self.players[0]
        highest_bid: int = 70
        highest_bidder: Player = None
        while True:
            current_player.hand = self.sort_cards(current_player.hand)
            bid = current_player.bid(highest_bid)
            if bid is None:
                if (
                    (highest_bidder is None)
                    and (current_player == self.players[-1])
                ):
                    # All players have passed and no bids have been placed,
                    # restart the bidding process
                    print('All players have passed. Restarting the game...')
                    self.deck = Deck()
                    self.play()
                    break
                else:
                    if ((highest_bidder is not None)
                        and (current_player == self.players[
                            (self.players.index(highest_bidder) + 3) % 4
                            ])):
                        # All players have passed, the highest bidder wins
                        # the bid
                        print(f'{highest_bidder} has won the bid with a bid \
                            of {highest_bid}.')
                        return (highest_bidder, highest_bid)
            elif int(bid) > highest_bid:
                highest_bid = int(bid)
                highest_bidder = current_player
                if bid == 250:
                    print(f'{highest_bidder} has won the bid with a capot.')
                    return (highest_bidder, highest_bid)
            else:
                print("Invalid bid. Please enter a higher bid or 'p' to pass.")
            current_player = self.players[
                (self.players.index(current_player) + 1) % len(self.players)]
        return (-1, -1)

    def sort_cards(self, cards: PileOfCard, trump_suit: str = None):
        """Sort a list of Card objects by suit and rank.

        If trump_suit is not None, cards are sorted first by whether or not
        they are the trump suit, then by rank within each suit. If trump_suit
        is None, cards are sorted first by suit, then by rank within each suit.

        Parameters:
        cards (list): The list of Card objects to sort.
        trump_suit (str): The trump suit.

        Returns:
        sorted_cards (list): The sorted list of Card objects.
        """
        sorted_cards: PileOfCard = []
        if trump_suit is not None:
            # Sort cards by trump suit first
            trump_cards: PileOfCard = [
                card for card in cards if card.suit == self.trump_suit]
            non_trump_cards: List[Card] = [
                card for card in cards if card.suit != self.trump_suit]
            # Sort trump suit cards by rank
            trump_cards.sort(key=lambda x: [
                'Jack', '9', 'Ace', '10', 'King', 'Queen', '8', '7']
                .index(x.rank))
            # Sort non-trump suit cards by suit
            non_trump_cards.sort(key=lambda x: x.suit)
            # Sort cards within each non-trump suit by rank
            for suit in ['Spades', 'Hearts', 'Clubs', 'Diamonds']:
                if suit == self.trump_suit:
                    continue
                suit_cards: List[Card] = [
                    card for card in non_trump_cards if card.suit == suit]
                suit_cards.sort(key=lambda x: [
                    'Ace', '10', 'King', 'Queen', 'Jack', '9', '8', '7']
                    .index(x.rank))
                # Replace sorted suit cards in the original list
                sorted_cards.extend(suit_cards)
            # Combine sorted trump and non-trump cards
            sorted_cards = trump_cards + sorted_cards
        else:
            # Sort cards by suit
            cards.sort(key=lambda x: x.suit)
            # Sort cards within each suit by rank
            for suit in ['Spades', 'Hearts', 'Clubs', 'Diamonds']:
                suit_cards: List[Card] = [
                    card for card in cards if card.suit == suit]
                suit_cards.sort(key=lambda x: [
                    'Jack', '9', 'Ace', '10', 'King', 'Queen', '8', '7']
                    .index(x.rank))
                # Replace sorted suit cards in the original list
                sorted_cards.extend(suit_cards)
        return sorted_cards

    def declare_trump(self, declarer):
        """Prompt the declarer to choose the trump suit."""
        trump_suit = None
        while trump_suit not in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            print(f'{declarer}, you have won the bid. Choose the trump suit \
                (Spades, Hearts, Diamonds, or Clubs):')
            trump_suit = input()
        print(f'The trump suit is {trump_suit}.')
        return trump_suit

    def play_trick(self, trick_num, trick_winner=None):
        """Play a trick of the game."""
        print(f'Playing trick {trick_num + 1}...')

        if trick_winner is None:
            # This is the first trick of the game, so the player 1 is the
            # first player
            indx_current_player = 0
        else:
            # The winner of the previous trick is the first player
            indx_current_player = self.players.index(trick_winner)

        trick = (PileOfCard(), trick_num+1)
        led_suit = None
        trick_winner: Player = None
        for player in (
                self.players[indx_current_player:]
                + self.players[:indx_current_player]):
            player.hand = self.sort_cards(player.hand, self.trump_suit)
            if led_suit is None:
                # This is the first card played in the trick, so the player
                # can play any card
                card = player.play_card(player.hand, f'This is the first card \
                    played in the trick, so {player} can play any card')
                trick[0].append(card)
                led_suit = card.suit
                trick_winner = player
                trick_winner_card = card
                trick_points = card.points(self.trump_suit)
            else:
                # This is not the first card played in the trick.
                trick, trick_points, trick_winner, trick_winner_card = (
                    self.playing_card(
                        player,
                        trick,
                        led_suit,
                        trick_points,
                        trick_winner,
                        trick_winner_card))
        print(f'{trick_winner} has won the trick with {trick_winner_card}.')
        print(f'{trick_winner} has won {trick_points} points.')
        self.players[
            self.players.index(trick_winner)].tricks_taken.append(trick)
        return trick_winner

    def playing_card(
            self,
            player: Player,
            trick: PileOfCard,
            led_suit: str,
            trick_points: int,
            trick_winner: Player,
            trick_winner_card: Card):
        """Play a card for a player in a trick.

        Parameters:
        player (Player): The player playing the card.
        trick (tuple): The current trick.
        led_suit (str): The suit of the first card played in the trick.
        trick_points (int): The points of the trick.
        trick_winner (Player): The player who has won the trick so far.
        trick_winner_card (Card): The card played by the trick winner.
        """
        print(f'The current trick is: {[trick[0]]}, \
            the led suit is {led_suit}, \
            and the trick points are {trick_points}.')
        print(f'The current trick winner is {trick_winner} \
            with the card {trick_winner_card}.')
        # The player must follow suit if they have a card of the led
        # suit
        if led_suit in [card.suit for card in player.hand]:
            if led_suit == self.trump_suit:
                # Create a list of trump cards in the player's hand.
                trump_cards = []
                for card in player.hand:
                    if card.suit == self.trump_suit:
                        trump_cards.append(card)
                if any([card.points(self.trump_suit)
                        > trick_winner_card.points(
                        self.trump_suit) for card in trump_cards]):
                    # If the player has a trump card that is higher
                    # than the current trick winner's card, they must
                    # play it
                    hand = [
                        card for card in player.hand
                        if ((card.suit == self.trump_suit)
                            and (card.points(
                                self.trump_suit)
                            > trick_winner_card.points(
                                self.trump_suit)))]
                    card = player.play_card(hand, "You must play a \
                        trump card that is higher than the current \
                            trick winner's card")
                else:
                    # If the player has no trump card that is higher
                    # than the current trick winner's card,
                    # they can play any trump card
                    hand = [card for card in player.hand if (
                        card.suit == self.trump_suit)]
                    msg = 'You must play a trump card.'
                    card = player.play_card(hand, msg)
            else:
                # The player has a card of the led suit, so they must
                # play a card of the led suit
                hand = [card for card in player.hand if card.suit == led_suit]
                msg = f'You must play a {led_suit}.'
                card = player.play_card(hand, msg)

        elif self.trump_suit in [card.suit for card in player.hand]:
            if player.teammate == trick_winner:
                # The player can play any card he wants if he has no card of
                # the led suit even if he has a trump card only if he's
                # teammate is the player which are currently winning the trick
                msg = f'You have no {led_suit}s. Your teammate is currently \
                    winning the trick. You can play any card you want.'
                card = player.play_card(player.hand, msg)
            else:
                # The player has no card of the led suit, but they have a
                # trump card, so they must play a trump card
                hand = [card for card in player.hand if (
                    card.suit == self.trump_suit)]
                msg = f'You have no {led_suit}s. You must play a trump card.'
                card = player.play_card(hand, msg)
        else:
            # The player has no card of the led suit or a trump card, so they
            # may play any card
            msg = f'You have no {led_suit}s or trump cards.'
            card = player.play_card(player.hand, msg)

        trick[0].append(card)
        trick_points += card.points(self.trump_suit)

        if card.suit == led_suit:
            if self.is_trump(card):
                # Trump card played, check if it is higher than the current
                # trick winner
                if (card.points(self.trump_suit)
                        > trick_winner_card.points(self.trump_suit)):
                    trick_winner = player
                    trick_winner_card = card
            else:
                # Non-trump card played, check if it is higher than the
                # current trick winner and that the winning card is not a
                # trump card
                is_higher = (
                    card.points(self.trump_suit)
                    > trick_winner_card.points(self.trump_suit))
                if is_higher and not self.is_trump(trick_winner_card):
                    trick_winner = player
                    trick_winner_card = card
        else:
            # Player has no card of the led suit, they may play any card
            if self.is_trump(card):
                # Trump card played, check if the curret winnig card is trump
                # and which is higher
                if not self.is_trump(trick_winner_card):
                    trick_winner = player
                    trick_winner_card = card
                elif (card.points(self.trump_suit)
                        > trick_winner_card.points(self.trump_suit)):
                    trick_winner = player
                    trick_winner_card = card
        return trick, trick_points, trick_winner, trick_winner_card

    def is_trump(self, card):
        """Return True if the card is a trump card, False otherwise."""
        return card.suit == self.trump_suit

    def calculate_points(self):
        """Calculate the points scored by each team in the current hand."""
        points = {player: 0 for player in self.players}
        # The last trick is 10 points worth
        player1 = self.players[0]
        player2 = self.players[1]
        player3 = self.players[2]
        player4 = self.players[3]
        if len(player1.tricks_taken) + len(player3.tricks_taken) == 8:
            # Team 1 (players 0 and 2) won all the tricks
            points[player1] += 250  # Capot bonus
            print(f'Team 1 (players {player1} and {player3}) won all the \
                tricks. They get a capot bonus of 250 points.')
        elif len(player2.tricks_taken) + len(player2.tricks_taken) == 8:
            # Team 2 (players 1 and 3) won all the tricks
            points[player2] += 250  # Capot bonus
            print(f'Team 2 (players {player2} and {player4}) won all the \
                tricks. They get a capot bonus of 250 points.')
        # Check for belote bonus
        for player in self.players:
            if player.belote():
                print(f'{player} has a belote: he gains the 20 points bonus.')
                points[player] += 20
        # Calculate tricks_taken points
        for player in self.players:
            # Give the 10 points of the last trick
            if 8 in [trick[1] for trick in player.tricks_taken]:
                print(f'{player} has taken the last trick: he gains the 10 \
                    points bonus.')
                points[player] += 10
            for trick in player.tricks_taken:
                points[player] += trick[0].calculate_points(self.trump_suit)
            print(f'{player} has scored {points[player]} points.')
        return points

    def print_results(self, points, bid, declarer):
        """Print the results of the current hand."""
        points = self.calculate_points()
        print(f'The bid was {bid} points with the trump {self.trump_suit}. \
            The declarer was {declarer}.')
        team1_points = points[self.players[0]] + points[self.players[2]]
        team2_points = points[self.players[1]] + points[self.players[3]]
        print(f'Team 1 (players {self.players[0]} and {self.players[2]}) \
            scored {team1_points} points.')
        print(f'Team 2 (players {self.players[1]} and {self.players[3]}) \
            scored {team2_points} points.')
        if declarer in [self.players[0], self.players[2]]:
            # Team 1 is the declarer
            if team1_points >= bid:
                print(f'Team 1 (players {self.players[0]} and \
                    {self.players[2]}) has won the hand.')
            else:
                print(f'Team 2 (players {self.players[1]} and \
                    {self.players[3]}) has won the hand.')
        else:
            # Team 2 is the declarer
            if team2_points >= bid:
                print(f'Team 2 (players {self.players[1]} and \
                    {self.players[3]}) has won the hand.')
            else:
                print(f'Team 1 (players {self.players[0]} and \
                    {self.players[2]}) has won the hand.')
