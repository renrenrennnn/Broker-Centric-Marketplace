import random
import numpy
import math

class CloudProvider(object):
    def __init__(self, ID, brokerSize):
        self._ID = ID
        self._brokerSize = brokerSize
        self._lowPrice = 0
        self._type2Price = 0
        self._highPrice = 0
        self._availableInstanceNum = 0
        self._D_bc = [1] * brokerSize
        self._D_cb = [1] * brokerSize
        self._D_bc_history = [[1 for col in range(brokerSize)]]
        self._B_in_history = [[1 for col in range(brokerSize)]]
        self._brokersCredit = [1] * brokerSize

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
    def D_bc(self):
        return self._D_bc
    @D_bc.setter
    def D_bc(self, newD_bc):
        self._D_bc = newD_bc

    @property
    def D_cb(self):
        return self._D_cb

    @property
    def brokersCredit(self):
        return self._brokersCredit

    @property
    def availableInstanceNum(self):
        return self._availableInstanceNum
    @availableInstanceNum.setter
    def availableInstanceNum(self, newAvailableInstanceNum):
        self._availableInstanceNum = newAvailableInstanceNum

    def genSupply(self):
        supply = numpy.random.default_rng().poisson(250)
        # print("lambda(cloud genSupply): ", supply)
        return supply

    def announcePrice(self):
        price = self._type2Price
        if self._availableInstanceNum < 140:
            price = round(self._type2Price * random.uniform(1.0, 1.6), 2)
        elif self._availableInstanceNum > 180:
            price = round(self._type2Price * random.uniform(0.4, 1.0), 2)
        return price

    def calBrokersCredit(self):
        sum_B_in = [sum(row) for row in zip(*self._B_in_history)]
        sum_D_bc = [sum(row) for row in zip(*self._D_bc_history)]
        # sum_B_in = [numpy.mean(row) for row in zip(*self._B_in_history)]
        # sum_D_bc = [numpy.mean(row) for row in zip(*self._D_bc_history)]
        print("sum of B_in", sum_B_in, "sum of D_bc", sum_D_bc)
        self._brokersCredit = [i / j for i, j in zip(sum_B_in, sum_D_bc)]

    def cal_D_cb(self, basic, brokerId):
        D_cb = basic + (self._availableInstanceNum - self._brokerSize * basic) * self._brokersCredit[brokerId] * (self._D_bc[brokerId] / sum(self._D_bc))
        print('Cloud', self._ID, 'give broker', brokerId, 'D_cb:', int(D_cb))
        if int(D_cb) > self._D_bc[brokerId]:
            D_cb = self._D_bc[brokerId]
        self._D_cb[brokerId] = int(D_cb)
        return int(D_cb)

    def updateBrokersCreditData(self, brokers):
        x = 20
        cur_D_bc = []
        cur_B_in = []
        for broker in brokers:
            cur_D_bc.append(self._D_bc[broker.ID])
            cur_B_in.append(self.D_cb[broker.ID])
        self._D_bc_history.insert(0, cur_D_bc)
        self._B_in_history.insert(0, cur_B_in)
        if len(self._D_bc_history) > x:
            self._D_bc_history.pop()
        if len(self._B_in_history) > x:
            self._B_in_history.pop()