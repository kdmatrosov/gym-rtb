import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random


class RtbEnv(gym.Env):
    def __init__(self, t=1000, b=1000):
        self.state = {}
        self.t = t
        self.b = b
        self.setState(t, b)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def setState(self, t, b):
        self.t = t
        self.b = b
        self.state['t'] = t
        self.state['b'] = b
        self.delta = .01

    def step(self, bid, winrate=10):
        bid = round(bid, 2)
        done = False
        reward = 0
        eps = random.random()
        if (eps < winrate/100) and (bid > 0) and (bid <= self.state['b']):
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
