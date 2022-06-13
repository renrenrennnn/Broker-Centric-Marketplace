from Broker import Broker
from CloudProvider import CloudProvider
from HistoryData import HistoryData
from User import User
from random import randrange, uniform
from numpy import *
import matplotlib.pyplot as plt
import logging

def main():
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='w', format=FORMAT)
    # g4 = HistoryData()
    # g5 = {1: 'apple', 2: 'banana00'}
    # g4.addUsersDemand(g5)
    # print(g4.userDemand)

    # --------------- #
    #     Initial     #
    # --------------- #
    m, n, k = 2, 2, 2 # Cloud, Broker, User
    clouds, brokers, users = [], [], []
    for idx in range(m):
        clouds.append( CloudProvider(idx, n) )
    for idx in range(n):
        brokers.append( Broker(idx, m, 1) )
    for idx in range(k):
        users.append( User(idx) )

    # ------------------------- #
    #     B-round(n) starts     #
    # ------------------------- #
    y = []
    y2 = []
    for b_round in range(2):
        print("------------------- round: ", b_round, "------------------")
        logging.info(f'-------------------round: {b_round}------------------')

        # User generage demand(step 1 -> done)
        for idx in range(k):
            users[idx].genDemand(n)

        # Broker aggregate all users' demand(step 1 -> done)
        logging.info(f'Broker aggregate all users demand')
        for idx in range(n):
            brokers[idx].aggregateDemand(users)
            print("broker", idx, "aggregate user demand sum:", brokers[idx].curUsersDemand)
            y.append(brokers[idx].curUsersDemand)

        # Broker decide D_bc (step 2 -> done)
        for brokerIdx in range(n):
            for cloudIdx in range(m):
                clouds[cloudIdx].D_bc[brokerIdx] = brokers[brokerIdx].cal_D_bc(cloudIdx)

        # Cloud reply instance supply and price (step 3 -> done)
        logging.info(f'Cloud reply instance supply and price')
        # for idx in range(n):
        #     cloud[0].type2Price = round(random.uniform(0.4, 0.6), 2)
        #     broker[idx].getCloudSupply(n, cloud[0])
        #     broker[idx].getCloudPrice(cloud[0])
        #     print("Broker", idx, "get from Cloud ", broker[idx].curCloudInstanceNum, "Instances")
        #     y2.append(broker[idx].curCloudInstanceNum)
        for cloud in clouds:
            cloud.type2Price = round(random.uniform(0.4, 0.6), 2)
            cloud.availableInstanceNum = cloud.genSupply()
            print('cloud',cloud.ID, 'available instance number:', cloud.availableInstanceNum)
        for broker in brokers:
            broker.getCloudSupply(clouds)
            broker.getCloudPrice(clouds)

        # Compare users' demand and cloud supply
        for idx in range(n):
            if brokers[idx].curUsersDemand <= brokers[idx].curCloudInstanceNum:
                print("profit-objective mode")
                logging.info('profit-objective mode')
                #################################################################
                #                    profit-objective mode                      #
                #################################################################
                print("broker", idx)
                for user in users:
                    # print("user sen:", user.priceSensitivity)
                    logging.info(f'user sensitivity: {user.priceSensitivity}')
                    maxProfit, optimalPrice, actualPurchase = brokers[idx].calMaxProfit(brokers[idx].curUsersDemand, 
                                                                                       user.priceSensitivity,
                                                                                       brokers[idx].curCloudPrice
                                                                                      )
                    logging.info(f'maximum profit: {maxProfit}, optimal price: {optimalPrice}, actualPurchase: {actualPurchase}')
                    # print("maxProfit:", maxProfit, "optimalPrice:", optimalPrice, "actualPurchase", actualPurchase)
            else:
                # print("fairness-objective mode")
                logging.info('fairness-objective mode')
        
    plt.plot(y, marker = 'o')
    plt.plot(y2, marker = 'o')
    plt.legend(['User demand', 'Cloud supply'])
    plt.show()
    
    logging.info('simulation done...')

if __name__ == '__main__':
    main()