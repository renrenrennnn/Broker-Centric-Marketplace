import numpy
from HistoryData import HistoryData
from User import User
import numpy as np

class Broker(object):
    def __init__(self, ID):
        self._ID = ID
        self._historyData = HistoryData()
        self._curCloudPrice = 0
        self._curCloudInstanceNum = 0
        self._curUsersDemand = 0
        self._cost = 0
        self._lowPrice = 0
        self._medPrice = 0
        self._highPrice = 0
        self._remainInstance = 0
        self.businessStrategyIndex = 1

    @property
    def ID(self):
        return self._ID
    @ID.setter
    def ID(self, newID):
        self._ID = newID
    
    @property
    def curUsersDemand(self):
        return self._curUsersDemand

    @property
    def curCloudInstanceNum(self):
        return self._curCloudInstanceNum

    @property
    def curCloudPrice(self):
        return self._curCloudPrice

    def aggregateDemand(self, users):
        # np.random.seed(0)
        totalUsersDemand = 0
        for idx in range(len(users)):
            totalUsersDemand = totalUsersDemand + users[idx].demand[self._ID] 
        self._curUsersDemand = totalUsersDemand

    def getCloudSupply(self, brokerSize, cloud):
        self._curCloudInstanceNum = cloud.genSupply()
    
    def getCloudPrice(self, cloud):
        self._curCloudPrice = cloud.announcePrice(self._curCloudInstanceNum)
        print("broker", self._ID, "get price", self._curCloudPrice)

    def calMaxProfit(self, baseDemand, priceSensitivity, cost):
        maxProfit = 0
        optimalPrice = 0
        for p in range(int(cost) + 1, baseDemand // priceSensitivity):
            profit = (baseDemand - priceSensitivity * p) * (p - cost)
            if profit > maxProfit:
                maxProfit = profit
                optimalPrice = p
        actualPurchase = baseDemand - priceSensitivity * optimalPrice
        return maxProfit, optimalPrice, actualPurchase

    # def calJainsFairnessIndex(self, usersSize, demand):
    #     x = 