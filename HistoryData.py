class HistoryData():
    
    def __init__(self, cloudSize, brokerSize, userSize, t):
        self._cloudSize = cloudSize
        self._brokerSize = brokerSize
        self._userSize = userSize
        self._t = t
        self._usersDemand = []
        self._usersActualTake = []
        self._retailPriceToUser = []
        self._wholesalePriceFromCloud = []
        self._othersInstanceNum = [[1 for col in range(self._brokerSize)] for row in range(self._cloudSize)]
        self._B_in = [1]
        self._B_out = [1]

    @property
    def cloudSize(self):
        return self._cloudSize
    
    @property
    def brokerSize(self):
        return self._brokerSize
    
    @property
    def userSize(self):
        return self._userSize

    @property
    def userDemand(self):
        return self._usersDemand
    def addUsersDemand(self, newUsersDemand):
        self._usersDemand.append(newUsersDemand)

    @property
    def usersActualTake(self):
        return self._usersActualTake
    def addUsersActualTake(self, newUsersActualTake):
        self._usersActualTake.append(newUsersActualTake)

    @property
    def retailPriceToUser(self):
        return self._retailPriceToUser
    def addRetailPrice(self, newRetailPrice):
        self._retailPriceToUser.append(newRetailPrice)

    @property
    def wholesalePriceFromCloud(self):
        return self._wholesalePriceFromCloud
    def addWholeSalePrice(self, newWholeSalePrice):
        self._wholesalePriceFromCloud.append(newWholeSalePrice)

    @property
    def othersInstanceNum(self):
        return self._othersInstanceNum
    def addOthersInstanceNum(self, newOthersInstanceNum):
        self._othersInstanceNum.append(newOthersInstanceNum)