import random
import numpy

class CloudProvider(object):
    def __init__(self, ID):
        self._ID = ID
        self._lowPrice = 0
        self._type2Price = 0
        self._highPrice = 0
        self._instanceNum = 0

    @property
    def ID(self):
        return self._ID
    @ID.setter
    def ID(self, newID):
        self._ID = newID
    
    @property
    def type2Price(self):
        return self._type2Price
    @type2Price.setter
    def type2Price(self, newPrice):
        self._type2Price = newPrice

    @property
    def instanceNum(self):
        return self._instanceNum

    def genSupply(self):
        supply = numpy.random.default_rng().poisson(160)
        print("lambda: ", supply)
        return supply

    def announcePrice(self, supply):
        price = self._type2Price
        if supply < 140:
            price = round(self._type2Price * random.uniform(1.0, 1.6), 2)
        elif supply > 180:
            price = round(self._type2Price * random.uniform(0.4, 1.0), 2)
        return price