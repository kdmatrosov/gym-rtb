# -*- coding: utf-8 -*-
from keras.models import load_model, model_from_json


class Dec_Keras:
    def __init__(self):
        self.PATH = "../keras"
        self.MODEL_PATH = "/model/"
        self.WEIGHTS_PATH = "/weights/"
        self.ARCHITECTURE_PATH = "/architecture/"

    def saveArchitecture(self, model, name):
        json_string = model.to_json()
        f = open(self.PATH + self.ARCHITECTURE_PATH + name + ".txt", "w")
        f.write(json_string)
        f.close()
        return 0

    def loadArchitecture(self, name):
        f = open(self.PATH + self.ARCHITECTURE_PATH + name + ".txt", "r")
        json_string = f.readline()
        f.close()
        return model_from_json(json_string)

    def saveModel(self, model, name):
        model.save(self.PATH + self.MODEL_PATH + name + '.h5')
        return 0

    def loadModel(self, name):
        return load_model(self.PATH + self.MODEL_PATH + name + '.h5')

    def saveWeights(self, model, name):
        model.save_weights(self.PATH + self.WEIGHTS_PATH + name + '.h5')

    def loadWeights(self, model, name):
        model.load_weights(self.PATH + self.WEIGHTS_PATH + name + '.h5')
        return model


