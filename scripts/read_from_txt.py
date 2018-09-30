# -*- coding: utf-8 -*-
import re
from hashlib import sha256


def hash(text):
    hashed = sha256(text.encode("UTF-8")).hexdigest()
    return hashed


f = open('../data1.txt', 'r')
data = f.readlines()
# print(re.findall(r'(\S+)', x[1]))
f.close()

f = open("../winrate.txt", "w")
data = data[1:]  # убрать первую строку

mapXtoWR = {}  # CTR

for line in data:
    x = re.findall(r'(\S+)', line)
    # key = hash(x[4] + "_" + x[5] + "_" + x[6])
    key = x[4] + "_" + x[5] + "_" + x[6]
    if key in mapXtoWR:
        mapXtoWR[key][0] += int(x[0])
        mapXtoWR[key][1] += int(x[1])
    else:
        mapXtoWR[key] = [int(x[0]), int(x[1]), 0]

line = "{:>5}\t {:>4}\t {:<4}% {:>30}\t" \
    .format("click", "show", "CTR", "user")
f.write(line + "\n")

for key in mapXtoWR:
    if mapXtoWR[key][1] > 0:
        mapXtoWR[key][2] = round(10000 * mapXtoWR[key][0] / mapXtoWR[key][1]) / 100
    line = "{:>5}\t {:>4}\t {:<6.2f} {:>30}" \
        .format(mapXtoWR[key][0], mapXtoWR[key][1], mapXtoWR[key][2], key)
    f.write(line + "\n")

f.close()
