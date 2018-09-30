import gym
from gym import error, spaces, utils
from gym.utils import seeding

class RtbEnv(gym.Env):

  def __init__(self):
      self.a = 1

  def step(self, action):
      return 0

  def reset(self):
      return 0