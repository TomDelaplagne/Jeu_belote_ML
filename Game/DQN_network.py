"""DQN network for the game."""

import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):
    """DQN network for the game."""
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x_input):
        """Forward pass of the network"""
        x_input = F.relu(self.layer1(x_input))
        x_input = F.relu(self.layer2(x_input))
        return self.layer3(x_input)
