import time
import pandas as pd
from pandas import DataFrame
import CreonApi
import copy
import StockProgram


def CompareDay():
    compareDiff = StockProgram.CompareDiff()
    compareDiff.ComparePrice()

def FirstStrategy():
    fistStrategy = StockProgram.FirstStrategy();
    fistStrategy.fistStrategy()

def SecondsStrategy():


FirstStrategy()
CompareDay()
