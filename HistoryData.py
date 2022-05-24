class HistoryData():
    
    def __init__(self):
        self._usersDemand = []
        self._usersActualTake = []
        self._retailPriceToUser = []
        self._wholesalePriceFromCloud = []
        self._othersInstanceNum = []


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
    def othersinstanceNum(self):
        return self._othersInstanceNum
    def addOthersInstanceNum(self, newOthersInstanceNum):
        self._othersInstanceNum.append(newOthersInstanceNum)