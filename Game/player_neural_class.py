import os
import copy

from deck_class import Deck
from player_class import Player, Dumb_Player
from game_class import BeloteGame
import numpy as np
from bid_class import Bid
import math

import torch
from torch import nn

dev = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using {dev} device")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Player_Neural(Player):
    def __init__(self, name : str, teammate=None, strategy=None):
        super().__init__(name, teammate)
        concatenated_array = strategy
        INPUT_NEURONS = 32
        FIRST_LAYER_HIDDEN_NEURONS = 16
        SECOND_LAYER_HIDDEN_NEURONS = 16
        output_neurons = 8
        matrix1_size = INPUT_NEURONS * FIRST_LAYER_HIDDEN_NEURONS
        matrix2_size = FIRST_LAYER_HIDDEN_NEURONS * SECOND_LAYER_HIDDEN_NEURONS
        matrix3_size = SECOND_LAYER_HIDDEN_NEURONS * output_neurons
        weigth_size = matrix1_size + matrix2_size + matrix3_size

        weigth_input_to_first_hidden = concatenated_array[:matrix1_size].reshape(INPUT_NEURONS, FIRST_LAYER_HIDDEN_NEURONS)
        weigth_first_to_second_hidden = concatenated_array[matrix1_size:matrix1_size + matrix2_size].reshape(FIRST_LAYER_HIDDEN_NEURONS, SECOND_LAYER_HIDDEN_NEURONS)
        weigth_second_hidden_to_output = concatenated_array[matrix1_size + matrix2_size:weigth_size].reshape(SECOND_LAYER_HIDDEN_NEURONS, output_neurons)

        self.first_hidden_bias = concatenated_array[weigth_size:weigth_size + FIRST_LAYER_HIDDEN_NEURONS]
        self.second_hidden_bias = concatenated_array[weigth_size + FIRST_LAYER_HIDDEN_NEURONS:weigth_size + FIRST_LAYER_HIDDEN_NEURONS + SECOND_LAYER_HIDDEN_NEURONS]
        self.output_bias = concatenated_array[weigth_size + FIRST_LAYER_HIDDEN_NEURONS + SECOND_LAYER_HIDDEN_NEURONS:]

        self.weigth = [weigth_input_to_first_hidden, weigth_first_to_second_hidden, weigth_second_hidden_to_output]
        self.bias = [self.first_hidden_bias, self.second_hidden_bias, self.output_bias]

    def __repr__(self):
        return super().__repr__() + " (Neural)"

    def play_card(self, hand, msg):
        # Neural network here
        if self.weigth is None:
            return hand[0]

        # create a numpy vector of the hand of the player
        hand_vector = np.zeros((32,1))
        for card in hand:
            suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
            non_trump = ["Ace", "10", "King", "Queen", "Jack", "9", "8", "7"]
            trump = ["Jack", "9", "Ace", "10", "King", "Queen", "8", "7"]
            suits.pop(suits.index(self.trump_suit))
            if card.suit == self.trump_suit:
                hand_vector[trump.index(card.rank)] = 1
            else:
                hand_vector[non_trump.index(card.rank) + 8 * (suits.index(card.suit) + 1)] = 1

        first_layer_network = sigmoid(np.matmul(hand_vector.T, self.weigth[0]) + self.bias[0])

        second_layer_network = sigmoid(np.matmul(first_layer_network, self.weigth[1]) + self.bias[1])

        last_layer = sigmoid(np.matmul(second_layer_network, self.weigth[2]) + self.bias[2])

        # find the index of the card to play
        index_card_to_play = np.argmax(last_layer) % len(hand)

        return hand[index_card_to_play]

    def bid(self, highest_bid: Bid) -> Bid or None:
        """Returns a bid or None if the player passes. Using Lancelot strategy. For the belote.fr website."""
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
        """Vérifie si les cartes sont dans la main de Lancelot."""
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
        """Compter le nombre d'As dans la main de Lancelot."""
        return sum(1 for card in self.hand if card.rank == 'A')

    def get_dict(self) -> dict:
        """Retourne un dictionnaire contenant les informations de Lancelot."""
        return {
            "name": self.name,
            "teammate": self.teammate.name if self.teammate else None,
            "hand": self.hand,
            "tricks_taken": [trick[0].get_dict() for trick in self.tricks_taken],
            "trump_suit": self.trump_suit
        }


class NeuralNetwork(nn.Module):
    """Neural network for the AI"""
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.ReLU()
        )

    def forward(self, x_input: torch.Tensor) -> torch.Tensor:
        """Forward pass of the neural network"""
        x_input = self.flatten(x_input)
        logits = self.linear_relu_stack(x_input)
        return logits

class NeuralNetworkTrainer:
    """Neural network trainer
    
    Attributes:
        model (NeuralNetwork): Neural network to train
        loss_fn (torch.nn.modules.loss): Loss function
        optimizer (torch.optim): Optimizer
        train_dataloader (torch.utils.data.dataloader.DataLoader): Training data
    
    Methods:
        train: Train the neural network
        test: Test the neural network
    """
    def __init__(self,
                 model: NeuralNetwork,
                 loss_fn: torch.nn.modules.loss,
                 optimizer: torch.optim,
                 num_decks: int = 1000):

        self.model = model
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.num_decks = num_decks

    def generate_decks(self, num_decks: int) -> list[Deck]:
        """Generate decks for training"""
        decks = []
        for _ in range(num_decks):
            deck = Deck()
            decks.append(deck)
        return decks

    def train(self):
        """Train the neural network from minimized loss for unsupervised learning by playing games and optimize the results"""
        decks = self.generate_decks(self.num_decks)

        results = torch.tensor([])
        current_deck_list = copy.deepcopy(decks)

        for deck in current_deck_list:
            Lancelot = Player_Neural("Lancelot")
            players: list[Player] = [Lancelot, Dumb_Player("Bob"), Dumb_Player("Fred"), Dumb_Player("David")]
            game = BeloteGame(players, deck)
            points = game.play()
            results.append(points[str(Lancelot)])
        
        loss = results.sum()
        # Convert results to tensor
        results = torch.tensor(results, dtype=torch.float32)
        results = results.view(-1, 1)

        # calculate loss
        loss = self.loss_fn(self.model(results), results)


class TreeSearcherPlayer(Player):
    """A player that uses a tree search algorithm to play cards."""
    def __init__(self, name: str):
        super().__init__(name)
        self.played_cards = []
        self.search_tree = {}  # initialize an empty search tree

    def play_card(self, hand, msg):
        """Play a card according to the search tree."""

        # if the search tree is empty, build it
        if not self.search_tree:
            self.build_search_tree(hand)


        max_utility = -math.inf
        for card in hand:
            utility = self.get_average_utility(card)
            if utility > max_utility:
                max_utility = utility
                card_to_play = card

        # add the played card to the list of played cards
        self.played_cards.append(card_to_play)
        # remove the played card from the hand
        hand.remove(card_to_play)
        # return the selected card
        return card_to_play

    def regret(self, card):
        """Calculate the regret of the card."""
        my_utility = self.get_average_utility(card)
        max_opponent_utility = -math.inf
        for opponent_card in self.opponent_possible_cards():
            utility = self.get_average_utility(opponent_card)
            if utility > max_opponent_utility:
                max_opponent_utility = utility
        return max_opponent_utility - my_utility

    def get_average_utility(self, card):
        """Calculate the average utility of playing the card."""
        if card in self.search_tree:
            node = self.search_tree[card]
            if node['plays'] > 0:
                return node['utility'] / node['plays']
        return 0  # if the card has not been played before, return 0

    def opponent_possible_cards(self):
        """Return a list of possible opponent cards."""
        # TODO: implement this method based on the game rules and current state
        pass

    def update_search_tree(self, card, utility):
        """Update the search tree with the result of playing the card."""
        if card not in self.search_tree:
            self.search_tree[card] = {'plays': 0, 'utility': 0}
        node = self.search_tree[card]
        node['plays'] += 1
        node['utility'] += utility
