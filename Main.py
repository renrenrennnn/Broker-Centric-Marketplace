from Broker import Broker
from CloudProvider import CloudProvider
from HistoryData import HistoryData
from User import User
from random import randrange, uniform
from numpy import *
import matplotlib.pyplot as plt

def main():
    # g4 = HistoryData()
    # g5 = {1: 'apple', 2: 'banana00'}
    # g4.addUsersDemand(g5)
    # print(g4.userDemand)

    # --------------- #
    #     Initial     #
    # --------------- #
    m, n, k = 1, 2, 2 # Cloud, Broker, User
    cloud, broker, users = [], [], []
    for idx in range(m):
        cloud.append( CloudProvider(idx) )
    for idx in range(n):
        broker.append( Broker(idx) )
    for idx in range(k):
        users.append( User(idx) )

    # ------------------------- #
    #     B-round(n) starts     #
    # ------------------------- #
    y = []
    y2 = []
    for b_round in range(10):
        print("--------------------round: ", b_round, "------------------")

        # Broker aggregate all users' demand
        for idx in range(n):
            broker[idx].aggregateDemand(n, k)
            print("broker", idx, "aggregate user demand sum:", broker[idx].curUsersDemand)
            y.append(broker[idx].curUsersDemand)

        # Cloud reply instance supply and price
        for idx in range(n):
            cloud[0].type2Price = round(random.uniform(0.4, 0.6), 2)
            broker[idx].getCloudSupply(n, cloud[0])
            broker[idx].getCloudPrice(cloud[0])
            print("Broker", idx, "get from Cloud ", broker[idx].curCloudInstanceNum, "Instances")
            y2.append(broker[idx].curCloudInstanceNum)

        # Compare users' demand and cloud supply
        for idx in range(n):
            if broker[idx].curUsersDemand <= broker[idx].curCloudInstanceNum:
                #######################################################################################
                #                                 profit-objective mode                               #
                #######################################################################################
                print("broker", idx)
                for user in users:
                    print("user sen:", user.priceSensitivity)
                    maxProfit, optimalPrice, actualPurchase = broker[idx].calMaxProfit(broker[idx].curUsersDemand, 
                                                                                       user.priceSensitivity,
                                                                                       broker[idx].curCloudPrice
                                                                                      )
                    print("maxProfit:", maxProfit, "optimalPrice:", optimalPrice, "actualPurchase", actualPurchase)
            else:
                print("fairness-objective mode")


        
    plt.plot(y, marker = 'o')
    plt.plot(y2, marker = 'o')
    plt.legend(['User demand', 'Cloud supply'])
    plt.show()

if __name__ == '__main__':
    main()