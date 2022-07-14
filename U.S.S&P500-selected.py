import pandas as pd
import numpy as np
import os

begintime = '2000-01-01'
endtime = '2020-12-31'


# Extract each stock's symbol from the original filename
def substr(str):
    a = str.index('_') + 1
    b = str.index('.')
    substr = str[a:b]
    return substr


def selecttime(time):
    if (time >= begintime) & (time <= endtime):
        return True
    else:
        return False


# Filter out the stocks that belong to the U.S. S&P 500
# in the U.S. stock and store their symbols in train_csv
df1 = pd.read_csv(r'C:\D\INTERCEPT\U.S.S&P500\U.S.S&P500-LIST.csv')
result = df1['Symbol'].values.tolist()
path = 'C:/D/INTERCEPT/US stock FQ/'
files = os.listdir(path)
train_csv = list(filter(lambda x: (x[-4:] == '.csv' and
                                   substr(x) in result), files))
# Take the union of the trading days of the U.S. S&P 500 stocks selected above,
# and store the trading days from 2000.01.01 to 2020.12.31 in time
time = []
for filename in train_csv:
    tmp = pd.read_csv(path + filename, encoding='gbk')['时间'].values.tolist()
    time.append(tmp)
uniontime = []
for t in time:
    uniontime = list(set(uniontime).union(set(t)))
print(len(uniontime))
uniontime.sort()
path2 = 'C:/D/INTERCEPT/U.S.S&P500/U.S.S&P500-selected/'
uniontime = list(filter(selecttime, uniontime))
print(len(uniontime))
print(uniontime)
# Find stocks that are not missing any trading day and
# store their sybols in name_out.csv
nameout_csv = []
for filename in train_csv:
    df = pd.read_csv(path + filename, encoding='gbk')
    stocktime = df['时间'].values.tolist()
    stocktime = list(filter(selecttime, stocktime))
    if (set(stocktime)) == (set(uniontime)):
        nameout_csv.append(filename)
# Change the column name of the original data of each stock
# in name_out.csv to form a new table
for filenameout in nameout_csv:
    df = pd.read_csv(path + filenameout, encoding='gbk')
    df.rename(columns={'时间': 'date', '开盘价(原始币种)': 'open',
                       '收盘价(原始币种)': 'close', '成交量(股)': 'volume'}, inplace=True)
    dataframe = df.loc[(df['date'] >= begintime) & (df['date'] <= endtime),
                       ['date', 'open', 'close', 'volume']]
# Determine if a stock has an opening or closing price
# less than $1 on a trading day
    if np.all(pd.notnull(dataframe)):
        df2 = dataframe.astype(str)
        df2['open'] = df2['open'].apply(lambda x: x.replace(',', ''))
        df2['close'] = df2['close'].apply(lambda x: x.replace(',', ''))
        openprice = df2['open'].values.tolist()
        closeprice = df2['close'].values.tolist()
# Determine if a stock has missing data
        if (all(float(i) >= 1 for i in openprice)) & \
                (all(float(i) >= 1 for i in closeprice)):
            dataframe.to_csv(path2 + filenameout, index=False, encoding="gbk")
