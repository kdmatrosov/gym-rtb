import gym
import numpy as np
import random
import gym_rtb
from win_rate import Win_Rate
from keras.models import Sequential
from keras.layers import Dense, InputLayer
import matplotlib.pylab as plt

winrate = Win_Rate()
win_data = winrate.getData("113_1_22_2_2")
win_data = float(win_data[2])

env = gym.make('Rtb-v0')
env.setState(t=1000, b=300, user='113_1_22_2_2', winrate=win_data)


def test_one(env, num_episodes=10):
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(1, 2)))
    model.add(Dense(300, activation='sigmoid'))
    model.add(Dense(700, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    list = []
    for i in range(num_episodes):
        minBid = 3.
        maxBid = 10.
        s = env.reset()
        done = False
        y = 0.95
        eps = 0.5
        decay_factor = 0.999
        delta = 0.01
        if i % 10 == 0:
            print("Episode {} of {}".format(i + 1, num_episodes))
        count = 0
        sum = 0
        while not done:
            count += 1
            stateNP = np.array([s['t'], s['b']]).reshape(1, 2)
            if np.random.random() < eps:
                bid = np.random.randint(0, int((maxBid - minBid) / delta)) * np.random.randint(0, 2)
            else:
                bid = np.argmax(model.predict(stateNP))

            new_s, r, done, _ = env.step(minBid + bid * delta)

            new_stateNP = np.array([new_s['t'], new_s['b']]).reshape(1, 2)

            target = r + y * np.max(model.predict(new_stateNP))
            target_vec = model.predict(stateNP)[0]
            target_vec[bid] = target
            model.fit(stateNP, target_vec.reshape(-1, 700), epochs=1, verbose=0)
            s = new_s
            # print(r, round(minBid + bid * delta, 2), s['b'])
            if (s['b'] < minBid):
                done = True
            sum += r
        list.append(sum / count)
    plt.plot(list)
    plt.ylabel('Average reward per game')
    plt.xlabel('Number of games')
    plt.show()
    return 0


test_one(env)

