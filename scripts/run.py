import gym
import re
import numpy as np
import random
import gym_rtb
from win_rate import Win_Rate
from dec_keras import Dec_Keras
from keras.models import Sequential
from keras.layers import Dense, InputLayer
import matplotlib.pylab as plt
import datetime

f = open('../data/test/set.txt', 'r')
data = f.readlines()
data = data[1:]  # убрать первую строку
f.close()
windata = []
for line in data:
    x = re.findall(r'(\S+)', line)
    windata.append([x[0], x[1], x[2], x[3], x[4], x[5]])

env = gym.make('Rtb-v0')
env.setState(t=1000, b=300)

decKeras = Dec_Keras()

delta = 0.01


# сделать подгрузку из файла по куче моделей
def test_one(env, num_episodes=300):
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
            # необходимо рандомить по одному объявлению, а не по всем сразу
            new_s, r, done, _ = env.step(minBid + bid * delta, float(windata[(np.random.randint(0, len(windata)))][2]))

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


# сделать подгрузку из файла по куче моделей
def test_two(env, num_episodes=1000, campId='1', advId='1'):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    __windata = list(filter(lambda x: x[3] == campId and x[4] == advId, windata))
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(1, 2)))
    model.add(Dense(300, activation='sigmoid'))
    model.add(Dense(300, activation='sigmoid'))
    model.add(Dense(700, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    model = decKeras.loadWeights(model, campId + "_" + advId)
    acc = []
    for i in range(num_episodes):
        minBid = 3.
        maxBid = 10.
        s = env.reset()
        done = False
        y = 0.95
        eps = 0.5
        # decay_factor = 0.999
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
            # необходимо рандомить по одному объявлению, а не по всем сразу
            new_s, r, done, _ = env.step(minBid + bid * delta,
                                         float(__windata[(np.random.randint(0, len(__windata)))][2]))

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
        acc.append(sum / count)
    decKeras.saveWeights(model, campId + "_" + advId)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    plt.plot(acc)
    plt.ylabel('Average reward per game')
    plt.xlabel('Number of games')
    plt.show()
    return 0


def train_model(env, campId='1', advId='1', minBid=3., maxBid=10., num_episodes=10):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print(campId, advId)
    __windata = list(filter(lambda x: x[3] == campId and x[4] == advId, windata))
    model = Sequential()
    nnMin = int(minBid / delta)
    nnMax = int(maxBid / delta)
    model.add(Dense(nnMin, activation='sigmoid'))
    model.add(Dense(nnMin, activation='sigmoid'))
    model.add(Dense(nnMax, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    model = decKeras.loadWeights(model, campId + "_" + advId)
    model = decKeras.loadWeights(model, campId + "_" + advId)
    acc = []
    for i in range(num_episodes):
        s = env.reset()
        done = False
        y = 0.95
        eps = 0.5
        # decay_factor = 0.999
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
            new_s, r, done, _ = env.step(minBid + bid * delta,
                                         float(__windata[(np.random.randint(0, len(__windata)))][2]))

            new_stateNP = np.array([new_s['t'], new_s['b']]).reshape(1, 2)

            target = r + y * np.max(model.predict(new_stateNP))
            target_vec = model.predict(stateNP)[0]
            target_vec[bid] = target
            model.fit(stateNP, target_vec.reshape(-1, nnMax), epochs=1, verbose=0)
            s = new_s
            # print(r, round(minBid + bid * delta, 2), s['b'])
            if (s['b'] < minBid):
                done = True
            sum += r
        acc.append(sum / count)
    decKeras.saveWeights(model, campId + "_" + advId)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

def test_model(env, campId='1', advId='1', minBid=3., maxBid=10., num_episodes=100):
    f = open('../data/train/set.txt', 'r')
    data = f.readlines()
    data = data[1:]  # убрать первую строку
    f.close()
    windata = []
    for line in data:
        x = re.findall(r'(\S+)', line)
        windata.append([x[0], x[1], x[2], x[3], x[4], x[5]])
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    __windata = list(filter(lambda x: x[3] == campId and x[4] == advId, windata))
    model = Sequential()
    nnMin = int(minBid / delta)
    nnMax = int(maxBid / delta)
    model.add(Dense(nnMin, activation='sigmoid'))
    model.add(Dense(nnMin, activation='sigmoid'))
    model.add(Dense(nnMax, activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    model = decKeras.loadWeights(model, campId + "_" + advId)
    model = decKeras.loadWeights(model, campId + "_" + advId)
    acc = []
    for i in range(num_episodes):
        s = env.reset()
        done = False
        y = 0.95
        eps = 0.5
        # decay_factor = 0.999
        if i % 10 == 0:
            print("Episode {} of {}".format(i + 1, num_episodes))
        count = 0
        sum = 0
        while not done:
            count += 1
            stateNP = np.array([s['t'], s['b']]).reshape(1, 2)
            bid = np.argmax(model.predict(stateNP))
            new_s, r, done, _ = env.step(minBid + bid * delta,
                                         float(__windata[(np.random.randint(0, len(__windata)))][2]))
            s = new_s
            if (s['b'] < minBid):
                done = True
            sum += r
        acc.append(sum / count)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    plt.plot(acc)
    plt.ylabel('Average reward per game')
    plt.xlabel('Number of games')
    plt.show()
    return 0


def callback_yad(env, num_episodes=1, campId='1', advId='1'):
    bid = 0.0
    return bid


for campX in range(1, 3):
    for advX in range(1, 3):
        train_model(env, str(campX), str(advX))
