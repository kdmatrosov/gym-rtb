import pickle
import re


class Pickle_Data:
    def readFromPickle(self, picklePath):
        with open(picklePath + ".pickle", 'rb') as f:
            data_new = pickle.load(f)
        return data_new

    def fromTxtToPickle(self, txtPath, picklePath):
        f = open(txtPath + ".txt", 'r')
        data = f.readlines()
        f.close()
        with open(picklePath + ".pickle", 'wb') as f:
            for line in data:
                x = re.findall(r'(\S+)', line)
                pickle.dump(x, f, pickle.HIGHEST_PROTOCOL)
