from Broker import Broker
from CloudProvider import CloudProvider
from HistoryData import HistoryData
from User import User
from random import randrange, uniform
from numpy import *
import matplotlib.pyplot as plt
import logging
import math

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
        users.append( User(idx, n) )

    # ------------------------- #
    #     B-round(n) starts     #
    # ------------------------- #
    y = []
    y2 = []
    for b_round in range(2):
        print("------------------- round: ", b_round, "------------------")
        logging.info(f'-------------------round: {b_round}------------------')

        # User generage demand(step 1 -> done)
        for user in users:
            user.genDemand(n)

        # Broker aggregate all users' demand(step 1 -> done)
        logging.info(f'Broker aggregate all users demand')
        for broker in brokers:
            broker.aggregateDemand(users)
            print("broker", broker.ID, "aggregate user demand sum:", broker.curUsersDemand)
            y.append(broker.curUsersDemand)

        # Broker decide D_bc (step 2 -> done)
        for broker in brokers:
            for cloud in clouds:
                cloud.D_bc[broker.ID] = broker.cal_D_bc(cloud.ID)

        # Cloud reply instance supply and price (step 3 -> done)
        logging.info(f'Cloud reply instance supply and price')
        for cloud in clouds:
            cloud.type2Price = round(random.uniform(0.4, 0.6), 2)
            cloud.availableInstanceNum = cloud.genSupply()
            print('cloud',cloud.ID, 'available instance number:', cloud.availableInstanceNum)
        for broker in brokers:
            broker.getCloudSupply(clouds)
            broker.getCloudPrice(clouds)
            # update broker's history data: other brokers' instance
            broker.updateHistoryData_othersInstanceNum(clouds, broker)

        # Compare users' demand and cloud supply
        for broker in brokers:
            if broker.curUsersDemand <= sum(broker.D_cb):
                print("profit-objective mode")
                logging.info('profit-objective mode')
                #################################################################
                #                    profit-objective mode                      #
                #################################################################
                # avgDemand = math.ceil(broker.curUsersDemand / m)
                # print("aveDemand: ", avgDemand)
                listOfCloudPrice = broker.curCloudPrice
                dictOfCloudPrice = {i : listOfCloudPrice[i] for i in range(0, len(listOfCloudPrice))}
                sortedCloudPrice = {k: v for k, v in sorted(dictOfCloudPrice.items(), key = lambda item: item[1])} # dict
                dictOf_D_cb = {i : broker.D_cb[i] for i in range(0, len(broker.D_cb))}
                # print("sorted cloud price:", sortedCloudPrice)
                for user in users:
                    # maxProfit, optimalPrice, actualPurchase = broker.calMaxProfit(broker.curUsersDemand, 
                    #                                                                    user.priceSensitivity,
                    #                                                                    min(broker.curCloudPrice)
                    #                                                                 )
                    keyListOfSortedCloudPrice = []
                    for k in sortedCloudPrice:
                        keyListOfSortedCloudPrice.append(k)
                    curIdx = 0
                    if user.demand[broker.ID] > dictOf_D_cb[keyListOfSortedCloudPrice[curIdx]]:
                        curIdx = curIdx + 1
                    maxProfit, optimalPrice, actualPurchase = broker.calMaxProfit(     user.demand[broker.ID], 
                                                                                       user.priceSensitivity,
                                                                                       broker.curCloudPrice[keyListOfSortedCloudPrice[curIdx]]
                                                                                 )
                    dictOf_D_cb[keyListOfSortedCloudPrice[curIdx]] = dictOf_D_cb[keyListOfSortedCloudPrice[curIdx]] - actualPurchase
                    logging.info(f'maximum profit: {maxProfit}, optimal price: {optimalPrice}, actualPurchase: {actualPurchase}')
                    print("maxProfit:", maxProfit, "optimalPrice:", optimalPrice, "actualPurchase", actualPurchase, "from cloud", keyListOfSortedCloudPrice[curIdx])
                    demandSatisfaction = user.calDemandSatisfaction(0.5, broker.ID, actualPurchase)
                    priceSatisfaction = user.calPriceSatisfaction(broker.ID, actualPurchase, optimalPrice, b_round + 2)
                    print("user", user.ID, "satis to broker", broker.ID, demandSatisfaction, priceSatisfaction)
                    user.update_D(broker.ID)
                    user.update_D_success(actualPurchase, broker.ID)
            else:
                print("fairness-objective mode")
                logging.info('fairness-objective mode')
        
    plt.plot(y, marker = 'o')
    plt.plot(y2, marker = 'o')
    plt.legend(['User demand', 'Cloud supply'])
    plt.show()
    
    logging.info('simulation done...')

if __name__ == '__main__':
    main()