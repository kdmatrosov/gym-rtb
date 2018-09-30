import gym
import gym_rtb

from win_rate import Win_Rate

winrate = Win_Rate()
print(winrate.getData("113_0_21"))

env = gym.make('Rtb-v0')
env.setState(t=1000, b=1000, user='113_0_21')
