# -*- coding: utf-8 -*-
import re


class Win_Rate:
    def __init__(self):
        f = open("../winrate.txt", "r")
        data = f.readlines()
        f.close()
        self.data = {}
        for line in data:
            x = re.findall(r'(\S+)', line)
            self.data[x[3]] = [x[0], x[1], x[2]]

    def getData(self, key):
        return self.data[key]
