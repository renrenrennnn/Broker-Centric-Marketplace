import numpy
from HistoryData import HistoryData
from User import User
import numpy as np
import statistics

class Broker(object):
    def __init__(self, ID, cloudSize, brokerSize, userSize, businessStrategyIndex):
        self._ID = ID
        self._cloudSize = cloudSize
        self._brokerSize = brokerSize
        self._userSize = userSize
        self._historyData = HistoryData(cloudSize, brokerSize, userSize, 2)
        self._curCloudPrice = [1] * cloudSize
        self._curCloudInstanceNum = 0
        self._curUsersDemand = 0
        self._cost = 0
        self._lowPrice = 0
        self._medPrice = 0
        self._highPrice = 0
        self._remainInstance = 0
        self._businessStrategyIndex = 1
        self._alpha = 1
        self._D_cb = [1] * cloudSize

    @property
    def ID(self):
        return self._ID
    @ID.setter
    def ID(self, newID):
        self._ID = newID

    
    # @property
    # def historyData(self):
    #     return self._historyData
    # @historyData.setter
    # def ID(self, newhistoryData):
    #     self._historyData = newhistoryData

    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, newCost):
        self._cost = newCost
    
    @property
    def D_cb(self):
        return self._D_cb
    @D_cb.setter
    def D_cb(self, new_D_cb):
        self._D_cb = new_D_cb

    @property
    def businessStrategyIndex(self):
        return self._businessStrategyIndex
    @businessStrategyIndex.setter
    def businessStrategyIndex(self, newBSI):
        self._businessStrategyIndex = newBSI

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

    def cal_D_bc(self, cloudId):
        alpha = self._alpha * self._businessStrategyIndex
        InstanceListInHistoryData = self._historyData.othersInstanceNum[cloudId]
        D_bc = int(alpha * self._curUsersDemand * (InstanceListInHistoryData[self._ID] / sum(InstanceListInHistoryData)))
        print('broker', self._ID, 'cloud', cloudId, 'D_bc = ', D_bc)
        return D_bc
    

    def getCloudSupply(self, clouds):
        basic = 50
        for cloud in clouds:
            self._D_cb[cloud.ID] = cloud.cal_D_cb(basic, self._ID)
    
    def getCloudPrice(self, clouds):
        for cloud in clouds:
            self._curCloudPrice[cloud.ID] = cloud.announcePrice()
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

    def updateHistoryData_othersInstanceNum(self, clouds, otherBroker):
        for cloud in clouds:
            self._historyData.othersInstanceNum[cloud.ID][otherBroker.ID] = self._historyData.othersInstanceNum[cloud.ID][otherBroker.ID] + sum(cloud.D_cb)

    
    def calJainsFairness(self, wholeInstance, users, brokerSize, brokerId):
        x_i = []
        for user in users:
            x_i.append(user.D_success[brokerId] / wholeInstance)
        fairness = (sum(x_i) ** 2) / (brokerSize * sum(x_i))

        return fairness