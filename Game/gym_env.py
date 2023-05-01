"""module for creating a custom gym environment"""

import gym
from gym import spaces

from game_class import BeloteGame
from player_class import Player

class BeloteGameEnv(gym.Env):
    """A class to represent a Belote game environment."""
    metadata = {}
    def __init__(self, *players: list[Player], deck = None):
        super().__init__()
        self.game = BeloteGame(*players, deck=deck)
        self.trick_played = 0
        self.trick_winner = None

        self.action_space = spaces.Discrete(2)

        # 2 token des cartes en main parmis 6 cartes ou 0 = 2:7
        # 3 token des cartes deja jouees ou 0 = 3:7

        # self.observation_space = spaces.MultiBinary([16, 17])
        self.observation_space = spaces.Box(low=0, high=6, shape=(5,), dtype=int)

    def step(self, action):
        """Play a trick of the game."""
        # action = 0, 1, 2, 3
        # 0 = play first card
        # 1 = play second card
        # 2 = play third card
        # 3 = play fourth card

        # Reward function:
        # - 50 if he plays a card that cannot be played
        # -1 if the trick is lost
        # +1 if the trick is won
        # -10 if the game is lost
        # +nb of point won if the game is won

        reward = 0
        done = False
        info = {}

        # Play a trick
        self.game.players[0].action = action
        try:
            self.trick_winner = self.game.play_trick(self.trick_winner)
        except IndexError:
            hand_observation = self.transform_card_list_to_token_list(self.game.players[0].hand, 2)
            played_cards_obs = self.transform_card_list_to_token_list(self.game.played_cards, 3)
            observation = hand_observation + played_cards_obs
            done = True
            reward = -50
            return observation, reward, done, info

        hand_observation = self.transform_card_list_to_token_list(self.game.players[0].hand, 2)
        played_cards_obs = self.transform_card_list_to_token_list(self.game.played_cards, 3)
        observation = hand_observation + played_cards_obs
        if self.trick_played == 2:
            done = True

            # Calculate and assign points
            points = self.game.calculate_points()

            if points.values[0] == max(points.values):
                reward = points[0]*5
                return observation, reward, done, info
            else:
                reward = -10
                return observation, reward, done, info


        if self.trick_winner == self.game.players[0]:
            reward = 1
            return observation, reward, done, info
        else:
            reward = -1
            return observation, reward, done, info

    def reset(self, seed=None, options=None):
        """Reset the environment."""
        super().reset(seed=seed)

        self.game = BeloteGame(*self.game.players)
        self.trick_played = 0
        self.trick_winner = None

        hand_observation = self.transform_card_list_to_token_list(self.game.players[0].hand, 2)
        played_cards_obs = self.transform_card_list_to_token_list(self.game.played_cards, 3)
        observation = hand_observation + played_cards_obs

        info = {}

        return observation, info

    def transform_card_to_token(self, card):
        suits = ["Hearts", "Spades", "Diamonds"]

        if card is None:
            return 0

        return suits.index(card.suit) * 2 + card.rank

    # def transform_card_to_token(self, card):
    #     """Transform a card to a token."""
    #     suits = ["Hearts", "Spades", "Diamonds", "Clubs"]

    #     token = [False for _ in range(17)]
    #     if card is None:
    #         token[-1] = True
    #         return token

    #     token[suits.index(card.suit) * 4 + card.rank] = True
    #     return token

    def transform_card_list_to_token_list(self, card_list, size_of_token_list):
        """Transform a list of cards to a list of tokens using the last to fill in order for the
        return to be a the size_of_token_list size."""
        token_list = [self.transform_card_to_token(card) for card in card_list]
        if len(token_list) > size_of_token_list:
            # troncate the list
            token_list = token_list[:size_of_token_list]
        for _ in range(size_of_token_list - len(token_list)):
            token_list.append(self.transform_card_to_token(None))
        return token_list
        