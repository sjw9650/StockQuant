import time
import pandas as pd
from pandas import DataFrame
import CreonApi
import copy


class DividStock(object) :

    def __init__(self, stockCode, price, stockName,dividend):
        print("divide")
        self.stockCode = stockCode
        self.price = price
        self.stockName = stockName
        self.dividend =dividend;

    def printStock(self):
        result = []
        result.append(self.stockCode)
        result.append(self.price)
        result.append(self.stockName)
        result.append(self.dividend)
        return result

class DivideStrategy():

    creon = CreonApi.Creon()
    codeinformList = [0,17]
    stockList = []
    # 0 종목코드, 4 현재가, 17 종목명, 20 : 총 상장주식수, 74 배당률, 75 부채비율, 77 ROA, 80 순이익증가율
    # 89 BPS, 91 영업이익 95 결산연월, 102 분기영업이익,107 분기 ROE, 111 결산연월  123 SPS 124 CFPS

    def refinedStock(self, inputdata):
        data = []
        lenofdata = len(inputdata)
        for index in range(lenofdata):
            tempdata = copy.deepcopy(inputdata[index])
            tempStock = DividStock(tempdata[0],tempdata[1],tempdata[2])
            self.stockList.append(tempStock)

    def saveDataStockList(self):
        lenofdata = len(self.stockList)
        result = []
        for index in range(lenofdata):
            result.append(self.stockList[index].printStock())
        df = DataFrame(result,columns=['종목코드', '종목명'])
        df.to_csv('StockList.csv')

    def dividStrategy(self):
        if self.creon.creonConnectCheck() == True:
            print("start")
            tempdata = self.creon.setAllStockList()
            sliceData = self.creon.dataSlice(tempdata)
            print("refinde")
            self.refinedStock(self.creon.subMarketEye(sliceData, self.codeinformList))
            print("saved")
            self.saveDataStockList()
            print("end")
        else:
            print("bye!")


def DivideStockList():
    divideStcok = DivideStrategy()
    divideStcok.dividStrategy()

DivideStockList()

