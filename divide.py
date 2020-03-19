import time
import pandas as pd
from pandas import DataFrame
import CreonApi
import copy


class DividStock(object) :

    creon = CreonApi.Creon()
    codeinformList = [0, 4, 17,73]
    stockList = []
    # 0 종목코드, 4 현재가, 17 종목명, 20 : 총 상장주식수, 74 배당률, 75 부채비율, 77 ROA, 80 순이익증가율
    # 89 BPS, 91 영업이익 95 결산연월, 102 분기영업이익,107 분기 ROE, 111 결산연월  123 SPS 124 CFPS

    def __init__(self, stockCode, price, stockName,dividend):
        print("divide")
        self.stockCode = stockCode
        self.price = price
        self.stockName = stockName
        self.dividend =dividend

    def refinedStock(self, inputdata):
        data = []
        lenofdata = len(inputdata)
        for index in range(lenofdata):
            tempdata = copy.deepcopy(inputdata[index])
            tempStock = Stock(tempdata[0],tempdata[1],tempdata[2],tempdata[3])
            self.stockList.append(tempStock)

    def saveDataStockList(self):
        lenofdata = len(self.stockList)
        result = []
        for index in range(lenofdata):
            result.append(self.stockList[index].printStock())
        df = DataFrame(result,columns=['종목코드', '현재가', '종목명', '배당금']
        df.to_csv('divideList.csv')

    def dividStrategy(self):
        if self.creon.creonConnectCheck() == True:
            tempdata = self.creon.setAllStockList()
            sliceData = self.creon.dataSlice(tempdata)
            self.refinedStock(self.creon.subMarketEye(sliceData, self.codeinformList))
            self.saveDataStockList()
        else:
            print("bye!")

def DivideStockList():
    divideStcok = DividStock()
    divideStcok.dividStrategy()

DivideStockList()

