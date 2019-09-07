import time
import win32com.client
import pandas as pd
from pandas import DataFrame
import copy

class Creon:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')

    def creonConnectCheck(self):
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            print("connect fail")
            return False
        else :
            return True

    def setAllStockList(self):
        # ## 대신 api 세팅
        obj = win32com.client.Dispatch("CpUtil.CpStockCode")
        numData = obj.GetCount()
        data = []
        self.numTotalCount = 0
        for index in range(numData):
            tempData = []
            tempData.append(obj.GetData(0, index))
            if  self.obj_CpCodeMgr.GetStockMarketKind(tempData[0]) == 1  or self.obj_CpCodeMgr.GetStockMarketKind(tempData[0]) == 2:
                data.append(tempData)

        return data;

    def dataSlice(self,stockList):
        refinedStockList = []
        stockCount = len(stockList);
        listRowCount = int(stockCount/200) + 1  #we just we 200 stock.. , so we need to slice the data.
        for i in range(listRowCount):
            tempList = []  # 안쪽 리스트로 사용할 빈 리스트 생성
            for j in range(200):
                numOfList = i*200 + j
                if stockCount <= numOfList :
                    break
                tempList.append(stockList[numOfList])  # 안쪽 리스트에 0 추가
            refinedStockList.append(tempList)
        return refinedStockList

    def subMarketEye(self, codeList, mInfoList):
        numCodeRow =len(codeList)
        print(numCodeRow)
        obj = win32com.client.Dispatch("cpsysdib.MarketEye")

        data=[]
        for index in range(numCodeRow):
            obj.SetInputValue(0, mInfoList)
            obj.SetInputValue(1, codeList[index])
            obj.BlockRequest()
            numField = obj.GetHeaderValue(0)
            numData = obj.GetHeaderValue(2)

            for idx_x in range(numData):
                tempdata=[]
                for idx_y in range(numField):
                    tempdata.append(obj.GetDataValue(idx_y, idx_x))
                data.append(tempdata)

        return data
