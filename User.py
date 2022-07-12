from multiprocessing import AuthenticationError
from random import randrange, uniform
from statistics import mean
import numpy as np
import math

class User(object):
    def __init__(self, ID, brokerSize):
        self._ID = ID
        self._brokerSize = brokerSize
        self._demand = []
        self._priceSensitivity = randrange(1, 4)
        self._demandSatisfaction = 1
        self._priceSatisfaction = 1
        self._D = [1] * brokerSize
        self._D_success = [1] * brokerSize
        self._retailPrice = [40] * brokerSize

    @property
    def ID(self):
        return self._ID
    @ID.setter
    def ID(self, newID):
        self._ID = newID
    
    @property
    def D(self):
        return self._D
    @D.setter
    def D(self, newD):
        self._D = newD
    @property
    def retailPrice(self):
        return self._retailPrice
    @retailPrice.setter
    def retailPrice(self, newRetailPrice):
        self._retailPrice = newRetailPrice

    @property
    def D_success(self):
        return self._D_success
    @D_success.setter
    def D_success(self, new_D_success):
        self._D_success = new_D_success

    @property
    def demandSatisfaction(self):
        return self._demandSatisfaction
    @demandSatisfaction.setter
    def demandSatisfaction(self, newSatisfaction):
        self._demandSatisfaction = newSatisfaction

    @property
    def priceSatisfaction(self):
        return self._priceSatisfaction
    @priceSatisfaction.setter
    def priceSatisfaction(self, newSatisfaction):
        self._priceSatisfaction = newSatisfaction

    @property
    def demand(self):
        return self._demand

    @property
    def priceSensitivity(self):
        return self._priceSensitivity
    
    def genDemand(self, brokerSize, curRound, arrivalRate):
        if curRound % 40 < 20:
            self._demand = np.random.default_rng().poisson(arrivalRate, brokerSize)
        else:
            self._demand = np.random.default_rng().poisson(arrivalRate * 2, brokerSize)
        print('user demand:', self._demand)

    def update_D(self, brokerId):
        self._D[brokerId] = self._D[brokerId] + self._demand[brokerId]
    
    def update_D_success(self, actualPurchase, brokerId):
            self._D_success[brokerId] = self._D_success[brokerId] + actualPurchase

    def calDemandSatisfaction(self, weight, brokerId, actualPurchase):
        historyRes = self._D_success[brokerId] / self._D[brokerId]
        curRes = actualPurchase / self._demand[brokerId]
        return historyRes * weight + curRes * (1 - weight)

    # def calPriceSatisfaction(self, brokerId, autualPurchase, optimalPrice, t):
    #     mean_D = (self._D[brokerId] + self._demand[brokerId]) / t
    #     meanRetailPrice = self._retailPrice[brokerId] / (t - 1)
    #     return (autualPurchase / mean_D) * (optimalPrice / meanRetailPrice)

    def calPriceSatisfaction(self, brokerId, autualPurchase, predefinedPrice, optimalPrice, t):
        S_PoS = math.exp((predefinedPrice - optimalPrice) / predefinedPrice)
        return S_PoS
