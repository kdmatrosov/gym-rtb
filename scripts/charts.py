from random import randint
import matplotlib.pylab as plt
print(randint(0, 9))
acc = []
for number in range(60):
    num = randint(0, 4) if randint(0, 7) == 0 else 0
    acc.append(num)
    print(num)

plt.plot(acc)
plt.ylabel('Клики')
plt.xlabel('Секунды')
plt.show()