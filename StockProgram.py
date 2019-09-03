import time
import win32com.client
import pandas as pd
from pandas import DataFrame
import copy

class StockProgram:
    def __init__(self):
        self.creonApi = creonApi;


    def refindeStockFirstStrategy(self, inputdata):
        data = []
        len2 = len(inputdata)
        for index in range(len2):
            tempdata = copy.deepcopy(inputdata[index])
            advantage = tempdata[12]
            advantage2 = tempdata[14]
            if advantage2 > 0 :
                per = tempdata[1]*tempdata[4] / (4 * advantage2)
                if advantage > 0 :
                    per2 = tempdata[1]*tempdata[4] / advantage

                    tempdata.append(per) ##19
                    debt = tempdata[7]
                    tempdata.append(debt)  ##20
                    if tempdata[11] > 0 :
                        pbr = tempdata[1] / tempdata[11]
                        tempdata.append(pbr)##21
                        roa = tempdata[9]
                        tempdata.append(roa)##22
                        sps = tempdata[19]
                        if sps > 0 :
                            psr = tempdata[1] /sps
                            tempdata.append(psr) ##23
                            cfps = tempdata[20]
                            if cfps > 0 :
                                pcr=tempdata[1] / cfps
                                tempdata.append(pcr)  ##24
                                if (per < 10) and (debt < 50)  and (pbr > 0.2) and(roa > 5) and(tempdata[10] > 0) :
                                    tempdata.append(0) #25
                                    tempdata.append(0) #26
                                    tempdata.append(0) #27
                                    tempdata.append(0) #28
                                    tempdata.append(0) #29
                                    data.append(tempdata)
        countData = len(data)
        data.sort(key=lambda x: x[21])
        for index in range(countData) :
            data[index][27] = index
            data[index][31] += index
        data.sort(key=lambda x: x[23])
        for index in range(countData) :
            data[index][28] = index
            data[index][31] += index
        data.sort(key=lambda x: x[25])
        for index in range(countData) :
            data[index][29] = index
            data[index][31] += index
        data.sort(key=lambda x: x[26])
        for index in range(countData) :
            data[index][30] = index
            data[index][31] += index

        data.sort(key=lambda x: x[31])
        return data

    def readCsvFile(self):
        csv_data = pd.read_csv('PrecodeList.csv', index_col=0)
        length = len(csv_data)
        for indx in range(length):
            self.codeListLast[indx] = csv_data['종목코드'][indx]

    def modifyArray(self,inputData):
        length = len(inputData)
        mylist = [0 for i in range(length)]

        for indx in range(length):
            mylist[indx] = inputData[indx][0]
        self.codeListLast = mylist

    def momenterm(self,m_InfoList):

        numCodeRow = len(self.codeListLast)
        print(numCodeRow)
        obj = win32com.client.Dispatch("cpsysdib.MarketEye")
        data = []
        obj.SetInputValue(0, m_InfoList)
        obj.SetInputValue(1, self.codeListLast)
        obj.BlockRequest()
        numField = obj.GetHeaderValue(0)
        numData = obj.GetHeaderValue(2)

        for idx_x in range(numData):
            tempdata = []
            for idx_y in range(numField):
                tempdata.append(obj.GetDataValue(idx_y, idx_x))
            if tempdata[4] > 0 :
                num5 = (tempdata[1] - tempdata[4]) / tempdata[4] * 100
            else :
                num5 = 0
            if tempdata[5] > 0:
                num10 = (tempdata[1] - tempdata[5]) / tempdata[5] * 100
            else:
                num10 = 0

            if tempdata[6] > 0:
                num20 = (tempdata[1] - tempdata[6]) / tempdata[6] * 100
            else:
                num20 = 0

            if tempdata[7] > 0:
                num60= (tempdata[1] - tempdata[7]) / tempdata[7] * 100
            else:
                num60 = 0

            tempdata.append(num5)
            tempdata.append(num10)
            tempdata.append(num20)
            tempdata.append(num60)
            data.append(tempdata)

        return data


if __name__ == "__main__":
    creon = Creon()
    if creon.creonConnectCheck() == 0 :
        exit()

    creon.getALLStockCode()
    m_InfoList =[0,4, 5, 17, 20, 67, 74, 75, 76,77, 80,89, 91, 95, 102, 107, 109, 110,111,123,124]
    creon.dataSlice()

    ### 자료가져오기
    data=creon.subMarketEye(m_InfoList)
    result = creon.refindeStock(data)

    df=DataFrame(result,  columns=['종목코드','현재가', '시가', '종목명', '총상장주식수', 'PER', '배당률', '부채비율', '유보율','ROA','순이익증가율','BPS','영업이익', '결산년월', '분기영업이익', '분기ROE', '분기유보율', '분기부채비율','최근분기년월','SPS','CFPS','per','debt','pbr','roa','psr','pcr','per_rank','pbr_rank','psr_rank','pcr_rank','sum_rank'])
    df.to_csv('codeList.csv')
    m_InfoList2 = [0,4,5,17,158,159,160,161]
    creon.modifyArray(result)
    result2 = creon.momenterm(m_InfoList2)
    df2 = DataFrame(result2,columns=['종목코드', '현재가', '시가', '종목명','5일 전 종가','10일 전 종가','20일 전 종가','60일 전 종가','5일 전 종가 Ratio','10일 전 종가 대비','20일 전 종가 대비' ,'60일 전 종가 대비'])
    df2.to_csv('codeListMomenterm.csv')
