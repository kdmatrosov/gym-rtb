import gym
from gym import error, spaces, utils
from gym.utils import seeding


class RtbEnv(gym.Env):
    def __init__(self, t=1000, b=1000, user="113_0_21", slip=0.2):
        print(t, b, user)
        self.t = t
        self.b = b
        self.slip = slip  # probability of 'slipping' an action
        self.setState(t, b, user)
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def setState(self, t, b, user):
        print(user)
        self.state = {
            t: t,
            b: b,
            user: user
        }
        self.delta = b / 100

    def step(self, bid):
        done = False
        reward = 0

        if (self.np_random.rand() < self.slip) and (bid <= self.state.b):
            self.state.b -= bid
            reward = 1

        self.state.t -= 1
        if (self.state.t == 0) or (self.state.b == 0):
            done = True
        return self.state, reward, done, self.delta

    def reset(self):
        self.state.t = self.t
        self.state.b = self.b
        return self.state
