from random import randint
import matplotlib.pylab as plt
import numpy as np

acc = []
acc2 = []
for number in range(60 * 24):
    max = 27
    rate = 100
    if number <= 500:
        max = 7
        if number < 400:
            max = 6
        if number > 100 and number < 300:
            max = 5
    else:
        if number < 800:
            max = 10
        if number < 700:
            max = 9
        if number < 600:
            max = 8
        max = 15 + randint(-1, 2)
        if number > 1000:
            max = 22
        if number > 1100:
            max = 27
        if number > 1150:
            max = 25
        if number > 1200:
            max = 22
        if number > 1250:
            max = 17
        if number > 1300:
            max = 12
        if number > 1350:
            max = 9
        max -= 2

    num = randint(-1 + int(max / 5), max + randint(-4, 5)) if randint(-1 + int(max / 5), rate) != 0 else 0
    acc.append(num)

acc2 = []
acc3 = []
i = 0
for number in range(0, 24):
    sum = 0
    for j in range(0, 60):
        sum = sum + acc[i]
        i = i + 1
    acc2.append(sum)
    acc3.append(sum + randint(sum * randint(12,13) + randint(-10, 50), sum * (randint(14, 17)) + randint(-50, 50)))

fig, ax1 = plt.subplots()
t = np.arange(0.01, 10.0, 0.01)
s1 = np.exp(t)
ax1.plot(acc2, 'b-')
ax1.set_xlabel('Часы')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Клики', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
s2 = np.sin(2 * np.pi * t)
ax2.plot(acc3, 'r-')
ax2.set_ylabel('Показы', color='r')
ax2.tick_params('y', colors='r')

fig.tight_layout()
plt.show()
