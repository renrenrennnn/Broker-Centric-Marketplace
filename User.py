from random import randrange, uniform
import numpy as np

class User(object):
    def __init__(self, ID):
        self._ID = ID
        # self._demand = np.random.default_rng().poisson(80, 1)
        self._demand = []
        self._priceSensitivity = randrange(1, 4)

    @property
    def ID(self):
        return self._ID
    @ID.setter
    def ID(self, newID):
        self._ID = newID

    @property
    def demand(self):
        return self._demand

    @property
    def priceSensitivity(self):
        return self._priceSensitivity
    
    def genDemand(self, brokerSize):
        self._demand = np.random.default_rng().poisson(80, brokerSize)
        print('user demand:', self._demand)