#! /usr/bin/python3

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, p2): # p1 == p2
        if p2 is None:
            return False
        return self.suit == p2.suit and self.rank == p2.rank

class Deck:
    def __init__(self):
        self.cards = []
        for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            for rank in ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7"]:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]

class Player:
    def __init__(self, name, teammate=None):
        self.name = name
        self.hand = []
        self.tricks_taken = []
        self.teammate = teammate
    
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

    def take_trick(self, trick):
        self.tricks_taken.append(trick)

    

class BeloteGame:
    def __init__(self, players: list[Player]):
        
        self.players = players
        for player in players:
            player.add_teammate(players[(players.index(player)+2)%4])
        self.deck = Deck()
        self.trump_suit = None

    def play(self):
        # Shuffle and deal cards
        self.deck.shuffle()
        hands = [self.deck.deal(8) for _ in self.players]
        for i, hand in enumerate(hands):
            self.players[i].hand = hand

        # Start the bidding
        (declarer, bid) = self.start_bidding()

        if (declarer == -1) and (bid == -1):
            # All players have passed, restart the game
            return

        # Declare the trump suit
        self.trump_suit = self.declare_trump(declarer)

        # Play the tricks
        trick_winner : Player = None
        for i in range(8):
            trick_winner = self.play_trick(i, trick_winner)

        # Calculate and assign points
        points = self.calculate_points()

        # Print the results
        self.print_results(points, bid, declarer)

    def start_bidding(self):
        """Prompt each player to bid or pass until a bid is accepted or all players pass."""
        print("Starting the bidding...")
        current_player = self.players[0]
        highest_bid = 0
        highest_bidder : Player = None
        while True:
            bid = None
            current_player.hand = self.sort_cards(current_player.hand)
            print(f"{current_player}, it is your turn to bid or pass. Your hand is: {current_player.hand}")
            while bid not in ["80", "90", "100", "110", "120", "130", "p"]:
                print(f"Enter your bid (80, 90, 100, 110, 120, or 130) or 'p' to pass:")
                bid = input()
            if bid == "p":
                if highest_bidder is None and current_player == self.players[-1]:
                    # All players have passed and no bids have been placed, restart the bidding process
                    print('All players have passed. Restarting the game...')
                    self.deck = Deck()
                    self.play()
                    break
                else:
                    print("You have passed.")
                    if (highest_bidder is not None) and (current_player == self.players[(self.players.index(highest_bidder)+3)%4]):
                        # All players have passed, the highest bidder wins the bid
                        print(f"{highest_bidder} has won the bid with a bid of {highest_bid}.")
                        return (highest_bidder, highest_bid)
            elif int(bid) > highest_bid:
                highest_bid = int(bid)
                highest_bidder = current_player
            else:
                print("Invalid bid. Please enter a higher bid or 'p' to pass.")
            current_player = self.players[(self.players.index(current_player) + 1) % len(self.players)]
            return (-1, -1)

    def sort_cards(self, cards, trump_suit=None):
        """Sort a list of Card objects by suit and rank.
        
        If trump_suit is not None, cards are sorted first by whether or not they are the trump suit,
        then by rank within each suit. If trump_suit is None, cards are sorted first by suit,
        then by rank within each suit.
        """
        sorted_cards = []
        if trump_suit!=None:
            # Sort cards by trump suit first
            trump_cards = [card for card in cards if card.suit == self.trump_suit]
            non_trump_cards = [card for card in cards if card.suit != self.trump_suit]
            # Sort trump suit cards by rank
            trump_cards.sort(key=lambda x: ["Jack", "9", "Ace", "10", "King", "Queen", "8", "7"].index(x.rank))
            # Sort non-trump suit cards by suit
            non_trump_cards.sort(key=lambda x: x.suit)
            # Sort cards within each non-trump suit by rank
            for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
                if suit == self.trump_suit:
                    continue
                suit_cards = [card for card in non_trump_cards if card.suit == suit]
                suit_cards.sort(key=lambda x: ["Ace", "10", "King", "Queen", "Jack", "9", "8", "7"].index(x.rank))
                # Replace sorted suit cards in the original list
                sorted_cards.extend(suit_cards)
            # Combine sorted trump and non-trump cards
            sorted_cards = trump_cards + sorted_cards
        else:
            # Sort cards by suit
            cards.sort(key=lambda x: x.suit)
            # Sort cards within each suit by rank
            for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
                suit_cards = [card for card in cards if card.suit == suit]
                suit_cards.sort(key=lambda x: ["Jack", "9", "Ace", "10", "King", "Queen", "8", "7"].index(x.rank))
                # Replace sorted suit cards in the original list
                sorted_cards.extend(suit_cards)
        return sorted_cards

    def declare_trump(self, declarer):
        """Prompt the declarer to choose the trump suit."""
        trump_suit = None
        while trump_suit not in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            print(f"{declarer}, you have won the bid. Choose the trump suit (Spades, Hearts, Diamonds, or Clubs):")
            trump_suit = input()
        print(f"The trump suit is {trump_suit}.")
        return trump_suit


    def play_trick(self, trick_num, trick_winner=None):
        """Play a trick of the game."""
        print(f"Playing trick {trick_num + 1}...")

        if trick_winner is None:
            # This is the first trick of the game, so the player 1 is the first player
            indx_current_player = 0
        else:
            # The winner of the previous trick is the first player
            indx_current_player = self.players.index(trick_winner)
        
        trick : list[list[Card]]= []
        led_suit= None
        trick_winner : Player = None
        trick_points = 0
        for player in self.players[indx_current_player:] + self.players[:indx_current_player]:
            player.hand = self.sort_cards(player.hand, self.trump_suit)
            if led_suit is None:
                # This is the first card played in the trick, so the player can play any card
                card = player.play_card(player.hand, f"This is the first card played in the trick, so {player} can play any card")
                trick.append(card)
                led_suit = card.suit
                trick_winner = player
                trick_winner_card = card
                trick_points += self.calculate_card_points(card)
            else:
                print(f"The current trick is: {trick}, the led suit is {led_suit}, and the trick points are {trick_points}.")
                print(f"The current trick winner is {trick_winner} with the card {trick_winner_card}.")
                # The player must follow suit if they have a card of the led suit
                if led_suit in [card.suit for card in player.hand]:
                    if led_suit == self.trump_suit:
                        trump_cards = [card for card in player.hand if card.suit == self.trump_suit]
                        if any([self.calculate_card_points(card) > self.calculate_card_points(trick_winner_card) for card in trump_cards]):
                            # If the player has a trump card that is higher than the current trick winner's card, they must play it
                            hand = [card for card in player.hand if card.suit == self.trump_suit and self.calculate_card_points(card) > self.calculate_card_points(trick_winner_card)]
                            card = player.play_card(hand, "You must play a trump card that is higher than the current trick winner's card")
                        else:
                            # If the player has no trump card that is higher than the current trick winner's card, they can play any trump card
                            card = player.play_card([card for card in player.hand if card.suit == self.trump_suit], "You must play a trump card.")
                    else:
                        card = player.play_card([card for card in player.hand if card.suit == led_suit], "You must follow suit.")

                elif self.trump_suit in [card.suit for card in player.hand]:
                    if player.teammate == trick_winner:
                        # The player can play any card he wants if he has no card of the led suit even if he has a trump card only if he's teammate is the player which are currently winning the trick
                        print(f"You have no {led_suit}s. Your teammate is currently winning the trick. You can play any card you want. Your cards are: {player.hand}")
                        print("Enter the rank and suit of the card you want to play (e.g. 'Queen of Spades'):")
                        while card == None or card not in player.hand or card.suit != self.trump_suit:
                            played_card = input()
                            card = Card(*played_card.split(" of ")[::-1])
                            if card not in player.hand:
                                print("Please enter a card that is in your hand.")
                    else:
                        # The player has no card of the led suit, but they have a trump card, so they must play a trump card
                        print(f"You have no {led_suit}s. Your trump cards are: {[card for card in player.hand if card.suit == self.trump_suit]}")
                        print("Enter the rank and suit of the card you want to play (e.g. 'Queen of Spades'):")
                        while card == None or card not in player.hand or card.suit != self.trump_suit:
                            played_card = input()
                            card = Card(*played_card.split(" of ")[::-1])
                            if card not in player.hand:
                                print("Please enter a card that is in your hand.")
                            elif card.suit != self.trump_suit:
                                print("You must play a trump card. Please enter a trump card.")
                else:
                    # The player has no card of the led suit or a trump card, so they may play any card
                    print(f"You have no {led_suit}s or trump cards. Your cards are: {player.hand}")
                    print("Enter the rank and suit of the card you want to play (e.g. 'Queen of Spades'):")
                    while card == None or card not in player.hand:
                        played_card = input()
                        card = Card(*played_card.split(" of ")[::-1])
                        if card not in player.hand:
                            print("Please enter a card that is in your hand.")

                player.hand.remove(card)
                trick.append(card)
                trick_points += self.calculate_card_points(card)

                if card.suit == led_suit:
                    if self.is_trump(card):
                        # Trump card played, check if it is higher than the current trick winner
                        if self.calculate_card_points(card) > self.calculate_card_points(trick_winner_card):
                            trick_winner = player
                            trick_winner_card = card
                    else:
                        # Non-trump card played, check if it is higher than the current trick winner and that the winning card is not a trump card
                        if self.calculate_card_points(card) > self.calculate_card_points(trick_winner_card) and not self.is_trump(trick_winner_card):
                            trick_winner = player
                            trick_winner_card = card
                else:
                    # Player has no card of the led suit, they may play any card
                    if self.is_trump(card):
                        # Trump card played, check if it is higher than the current trick winner
                        if self.calculate_card_points(card) > self.calculate_card_points(trick_winner_card):
                            trick_winner = player
                            trick_winner_card = card
        print(f"{trick_winner} has won the trick with {trick_winner_card}.")
        print(f"{trick_winner} has won {trick_points} points.")
        self.players[self.players.index(trick_winner)].tricks_taken.append(trick)
        return trick_winner

    def is_trump(self, card):
        """Return True if the card is a trump card, False otherwise."""
        return card.suit == self.trump_suit

    def calculate_points(self):
        """Calculate the points scored by each team in the current hand."""
        points = {player: 0 for player in self.players}
        if len(self.players[0].tricks_taken) + len(self.players[2].tricks_taken) == 8:
            # Team 1 (players 0 and 2) won all the tricks
            points[self.players[0]] += 250  # Capot bonus
            points[self.players[2]] += 250
            print(f"Team 1 (players {self.players[0]} and {self.players[2]}) won all the tricks. They get a capot bonus of 250 points.")
        elif len(self.players[1].tricks_taken) + len(self.players[1].tricks_taken) == 8:
            # Team 2 (players 1 and 3) won all the tricks
            points[self.players[1]] += 250  # Capot bonus
            points[self.players[3]] += 250
            print(f"Team 2 (players {self.players[1]} and {self.players[3]}) won all the tricks. They get a capot bonus of 250 points.")
        # Check for belote bonus
        for player in self.players:
            if "King" in [card.rank for card in player.hand if self.is_trump(card)] and "Queen" in [card.rank for card in player.hand if self.is_trump(card)]:
                points[player] += 20  # Belote bonus
                print(f"{player} has a belote. They get a bonus of 20 points.")
        # Calculate individual card points
        for player in self.players:
            for card in player.hand:
                points[player] += self.calculate_card_points(card)
        print(points)
        return points
    
    def calculate_card_points(self, card):
        """Calculate the points scored by a single card in the Belote game."""
        if card.suit == self.trump_suit:
            # Card is a trump card
            if card.rank == "Ace":
                return 11
            elif card.rank == "10":
                return 10
            elif card.rank == "King":
                return 4
            elif card.rank == "Queen":
                return 3
            elif card.rank == "Jack":
                return 20
            elif card.rank == "9":
                return 14
            else:
                return 0
        else:
            # Card is not a trump card
            if card.rank == "Ace":
                return 11
            elif card.rank == "10":
                return 10
            elif card.rank == "King":
                return 4
            elif card.rank == "Queen":
                return 3
            elif card.rank == "Jack":
                return 2
            else:
                return 0

    def print_results(self, points, bid, declarer):
        """Print the results of the current hand."""
        points = self.calculate_points()
        team1_points = points[self.players[0]] + points[self.players[2]]
        team2_points = points[self.players[1]] + points[self.players[3]]
        print(f"Team 1 (players {self.players[0]} and {self.players[2]}) scored {team1_points} points.")
        print(f"Team 2 (players {self.players[1]} and {self.players[3]}) scored {team2_points} points.")
        if declarer in [self.players[0], self.players[2]]:
            # Team 1 is the declarer
            if team1_points >= bid:
                print(f"Team 1 (players {self.players[0]} and {self.players[2]}) has won the hand.")
            else:
                print(f"Team 2 (players {self.players[1]} and {self.players[3]}) has won the hand.")
        else:
            # Team 2 is the declarer
            if team2_points >= bid:
                print(f"Team 2 (players {self.players[1]} and {self.players[3]}) has won the hand.")
            else:
                print(f"Team 1 (players {self.players[0]} and {self.players[2]}) has won the hand.")


def main():
    game = BeloteGame([Player("Alice"), Player("Bob"), Player("Charlie"), Player("David")])
    game.play()

if __name__ == "__main__":
    main()