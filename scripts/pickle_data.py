import pickle


class Pickle_data:
    def readFromPickle(self, picklePath):
        with open(picklePath + ".pickle", 'rb') as f:
            data_new = pickle.load(f)
        return data_new

    def fromTxtToPickle(txtPath, picklePath):
        f = open(txtPath + ".txt", 'r')
        data = f.readlines()
        f.close()
        with open(picklePath + ".pickle", 'wb') as f:
            pickle.dump(data, f)
