import gym
import gym_rtb
from win_rate import Win_Rate

winrate = Win_Rate()
print(winrate.getData("113_1_22_2_2"))

env = gym.make('Rtb-v0')
env.setState(t=1000, b=1000, user='113_1_22_2_2')

def test_one(env, num_episodes=500):
    for i in range(num_episodes):
        s = env.reset()
        done = False
        while not done:
            new_s, r, done, _ = env.step(10)
            s = new_s
    return 0


test_one(env)
