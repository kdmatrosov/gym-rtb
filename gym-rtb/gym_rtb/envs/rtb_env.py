import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random


class RtbEnv(gym.Env):
    def __init__(self, t=1000, b=1000, user="113_1_22_2_2", winrate=10):
        self.state = {}
        self.t = t
        self.b = b
        self.winrate = winrate  # probability of 'slipping' an action
        self.setState(t, b, user, winrate)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def setState(self, t, b, user, winrate):
        self.winrate = winrate / 100
        self.t = t
        self.b = b
        self.state['t'] = t
        self.state['user'] = user
        self.state['b'] = b
        self.delta = .01

    def step(self, bid):
        bid = round(bid, 2)
        done = False
        reward = 0
        eps = random.random()
        if (eps < self.winrate) and (bid > 0) and (bid <= self.state['b']):
            self.state['b'] -= bid
            reward = 1

        self.state['t'] -= 1
        if (self.state['t'] == 0) or (self.state['b'] == 0):
            done = True
        return self.state, reward, done, self.delta

    def reset(self):
        self.state['t'] = self.t
        self.state['b'] = self.b
        return self.state
