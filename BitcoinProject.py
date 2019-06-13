import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

dataset1 = pd.read_csv('ALLTweets.csv',delimiter=",")
dataset2 = pd.read_csv('BTC-USD_CBPrices.csv')


prices = dataset2[['Date','open','close']]
prices['Date'] = pd.to_datetime(prices.Date, unit='s')
prices = prices.sort_values(by=['Date'])


##validating hour to hour data
train, test = train_test_split(prices, test_size=0.2,shuffle=False)
prices=test
prices['price_fluct']=(prices['close']-prices['open'])/prices['open']
for i in prices.index:
    if prices.at[i,'price_fluct'] > 0.001:
        prices.at[i,'price_fluct'] = 1
    elif prices.at[i,'price_fluct'] < -0.001:
        prices.at[i,'price_fluct'] = -1
    else:
        prices.at[i,'price_fluct'] = 0
prices['price_fluct']=prices['price_fluct'].astype(int)
target_series=prices.filter(['Date','price_fluct'], axis=1)
target_series['NPrice']=target_series['price_fluct'].shift(1)
target_series=target_series.dropna()
target_series['result'] = np.where(target_series['price_fluct'] == target_series['NPrice'], 1, 0)
Correct=target_series['result'].sum()
total= target_series.shape[0]
accuracy = (Correct/total)*100
print (f"Accuracy when Data is in hours format is: {accuracy}")