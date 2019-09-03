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
        self.codeList = []
        self.totalInfoList = []
        self.numTotalCount = 0
        self.codeListLast = []
