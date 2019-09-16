import time
import pandas as pd
from pandas import DataFrame
import CreonApi
import copy

class Stock(object) :

    def __init__(self, stockCode, price, stockName, maketCap, dividendRate, debt,roa, bps, operatingIncome, sps, cps):
        self.stockCode = stockCode
        self.price = price
        self.stockName = stockName
        self.dividendRate =dividendRate
        self.operatingIncome = operatingIncome * 4 * 0.95 # 전분기 영업이익 *4 * 0.95
        self.debt = debt

        if operatingIncome != 0:
            self.per = (maketCap * price) / operatingIncome
        else :
            self.per = 0.0

        if sps != 0:
            self.psr = price / sps
        else :
            self.psr = 0.0

        if cps != 0 :
            self.pcr = price / cps
        else :
            self.pcr = 0.0
        if bps != 0 :
            self.pbr = price / bps
        else :
            self.pbr = 0.0

        self.roa = roa
        self.psrRank = 0
        self.pbrRank = 0
        self.perRank = 0
        self.pcrRank = 0
        self.totalRank = 0

    def setPsrRank(self,rank):
        self.psrRank = rank
    def setPbrRank(self,rank):
        self.pbrRank = rank
    def setPerRank(self,rank):
        self.perRank = rank
    def setPcrRank(self,rank):
        self.pcrRank = rank
    def setTotalRank(self,rank):
        self.totalRank = self.totalRank + rank

    def printStock(self):
        result = []
        result.append(self.stockCode)
        result.append(self.price)
        result.append(self.stockName)
        result.append(self.dividendRate)
        result.append(self.operatingIncome)
        result.append(self.debt)
        result.append(self.roa)
        result.append(self.per)
        result.append(self.psr)
        result.append(self.pcr)
        result.append(self.pbr)
        result.append(self.perRank)
        result.append(self.psrRank)
        result.append(self.pcrRank)
        result.append(self.pbrRank)
        result.append(self.totalRank)
        return result

class CompareDiff(object):
    creon = CreonApi.Creon()
    codeinformList = [0, 4, 17]
    stockList = []
    diffList = []

    def __init__(self):
        print("CompareDiff Class Init")

    def readCsvFile(self):
        csv_data = pd.read_csv('PrecodeList.csv', index_col=0)
        length = len(csv_data)
        print (length)
        for indx in range(length):
            tempList = []
            tempList.append(csv_data['종목코드'][indx])
            tempList.append(csv_data['종목명'][indx])
            tempList.append(csv_data['현재가'][indx])
            self.stockList[indx] = csv_data['종목코드'][indx]
            slef.diffList.append(tempList)
        df = DataFrame(self.diffList,columns=['종목코드', '종목명', '현재가'])
        df.to_csv('test.csv')
        print (len(self.stockList))

    def ComparePrice(self):
        if self.creon.creonConnectCheck() == True :
            quant.refinedStock(quant.creon.subMarketEye(self.stockList, self.codeinformList))
            print
        else:
            print("bye!")




class FirstStrategy(object):
    creon = CreonApi.Creon()
    codeinformList = [0, 4, 17, 20, 74, 75, 77, 80, 89, 91, 95, 102, 107, 111, 123, 124]
    stockList = []

    # 0 종목코드, 4 현재가, 17 종목명, 20 : 총 상장주식수, 74 배당률, 75 부채비율, 77 ROA, 80 순이익증가율
    # 89 BPS, 91 영업이익 95 결산연월, 102 분기영업이익,107 분기 ROE, 111 결산연월  123 SPS 124 CFPS

    def __init__(self):
        print("init FirstStarategy")

    def saveDataStockList(self):
        lenofdata = len(self.stockList)
        result = []
        for index in range(lenofdata):
            result.append(self.stockList[index].printStock())
        df = DataFrame(result,columns=['종목코드', '현재가', '종목명', '배당률', '영업이익','부채비율','ROA','per','psr','pcr','pbr','perRanK','psrRanK','pcrRanK','pbrRanK','totalRank'])
        df.to_csv('codeList2.csv')

    def refinedStock(self, inputdata):
        data = []
        lenofdata = len(inputdata)
        for index in range(lenofdata):
            tempdata = copy.deepcopy(inputdata[index])
            tempStock = Stock(tempdata[0],tempdata[1],tempdata[2],tempdata[3],tempdata[4],tempdata[5],tempdata[6],tempdata[8],tempdata[11],tempdata[14],tempdata[15])
            if (tempStock.per < 15) and (tempStock.per > 0) and (tempStock.debt < 50)  and (tempStock.pbr > 0.2) and(tempStock.roa > 4) :
                self.stockList.append(tempStock)

    def sortList(self):
        countData = len(self.stockList)
        self.stockList.sort(key=lambda x: x.psr)
        for index in range(countData):
            self.stockList[index].setPsrRank(index)
            self.stockList[index].setTotalRank(index)

        self.stockList.sort(key=lambda x: x.pbr)
        for index in range(countData):
            self.stockList[index].setPbrRank(index)
            self.stockList[index].setTotalRank(index)

        self.stockList.sort(key=lambda x: x.per)
        for index in range(countData) :
            self.stockList[index].setPerRank(index)
            self.stockList[index].setTotalRank(index)

        self.stockList.sort(key=lambda x: x.pcr)
        for index in range(countData) :
            self.stockList[index].setPcrRank(index)
            self.stockList[index].setTotalRank(index)

        self.stockList.sort(key=lambda x: x.totalRank)

if __name__ == "__main__":
    quant = FirstStrategy()
    if quant.creon.creonConnectCheck() == True :
        tempdata = quant.creon.setAllStockList()
        sliceData = quant.creon.dataSlice(tempdata)
        quant.refinedStock(quant.creon.subMarketEye(sliceData, quant.codeinformList))
        quant.sortList()
        quant.saveDataStockList()
    else:
        print("bye!")
