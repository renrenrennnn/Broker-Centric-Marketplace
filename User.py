from random import randrange, uniform

class User(object):
    def __init__(self, ID):
        self._ID = ID
        self._demand = randrange(10, 90)
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
    # @demand.setter
    # def demand(self, newDemand):
    #     self._demand = newDemand

    # def genDemand(-