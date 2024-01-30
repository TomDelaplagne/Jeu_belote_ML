
import torch
import matplotlib.pyplot as plt

from itertools import count

from training import Trainer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():
    """Main function for the game."""
    if torch.cuda.is_available():
        num_episodes = 600
    else:
        num_episodes = 10_000

    trainer = Trainer()

    for _ in range(num_episodes):
        # Initialize the environment and get it's state
        state, _ = trainer.env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        for t in count():
            action = trainer.select_action(state)
            observation, reward, done, _ = trainer.env.step(action.item())
            reward = torch.tensor([reward], device=device)

            if done:
                next_state = None
            else:
                next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

            # Store the transition in memory
            trainer.memory.push(state, action, next_state, reward)

            # Move to the next state
            state = next_state

            # Perform one step of the optimization (on the policy network)
            trainer.optimize_model()

            # Soft update of the target network's weights
            # θ′ ← τ θ + (1 −τ )θ′
            target_net_state_dict = trainer.target_net.state_dict()
            policy_net_state_dict = trainer.policy_net.state_dict()
            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[key]*trainer.TAU + target_net_state_dict[key]*(1-trainer.TAU)
            trainer.target_net.load_state_dict(target_net_state_dict)

            if done:
                trainer.episode_durations.append(t + 1)
                trainer.plot_durations()
                break

    print('Complete')
    trainer.plot_durations(show_result=True)
    plt.ioff()
    plt.show()

if __name__ == '__main__':
    main()