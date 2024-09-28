import torch
import torch.nn as nn
import torch.nn.functional as F
#import utils

def __compute_discounted_rewards__(rewards, gamma, device):
    cum_rewards = torch.zeros((rewards.shape[0])).to(device)
    reward_len = len(rewards)
    for j in reversed(range(reward_len)):
        cum_rewards[j] = rewards[j] + (cum_rewards[j+1]*gamma if j+1 < reward_len else 0)
    return cum_rewards

class A2CAgent():
    def __init__(self, sdim:int, adim:int, hdim:int = 16, gamma = 0.99, lr:float = 0.001,
                 actor_model = None, critic_model = None, device = 'cpu'):
        self.gamma = gamma

        self.device = device

        if actor_model is not None:
            self.actor = actor_model
        else:
            self.actor = nn.Sequential(
                nn.Linear(sdim, hdim),
                nn.ReLU(),
                nn.Linear(hdim, adim)
            )
        
        if critic_model is not None:
            self.critic = critic_model
        else:
            self.critic = nn.Sequential(
                nn.Linear(sdim, hdim),
                nn.ReLU(),
                nn.Linear(hdim, 1)
            )

        self.actor.to(device)
        self.critic.to(device)

        self.opt_actor = torch.optim.Adam(self.actor.parameters(), lr=lr)
        self.opt_critic = torch.optim.Adam(self.critic.parameters(), lr=lr)

    def act(self, state):
        with torch.no_grad():
            logits = self.actor(state)
        probs = F.softmax(logits, dim=1)
        action = torch.multinomial(probs, num_samples=1)[0].item()
        return action
    
    def train(self, states, actions, rewards):
        states = torch.stack(states).squeeze(1)
        rewards = torch.tensor(rewards)

        # critic loss
        self.opt_critic.zero_grad()
        discounted_rewards = __compute_discounted_rewards__(rewards, self.gamma, self.device)
        values = self.critic(states).squeeze(1)
        critic_loss = F.mse_loss(values, discounted_rewards, reduction='none')
        critic_loss.sum().backward()
        self.opt_critic.step()

        # actor loss
        self.opt_actor.zero_grad()
        with torch.no_grad():
            values = self.critic(states).squeeze(1)
        actions = torch.tensor(actions).to(self.device)
        advantages = discounted_rewards - values
        logits = self.actor(states)
        log_probs = -F.cross_entropy(logits, actions, reduction='none')
        actor_loss = -log_probs * advantages
        actor_loss.sum().backward()
        self.opt_actor.step()
        
        return actor_loss.sum().item(), critic_loss.sum().item(), rewards.sum().item()
    
if __name__ == '__main__':
    agent = A2CAgent()