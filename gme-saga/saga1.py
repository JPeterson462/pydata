import pandas as pd
import utils
import numpy as np
import scipy.stats

# Load dataframes
stock_prices = pd.read_csv('Download Data - STOCK_US_XNYS_GME.csv')
stock_prices = stock_prices[["Date","Open","Close"]]
wsb_daily_volume = pd.read_csv('wsb_daily_volume.csv')
wsb_daily_volume = wsb_daily_volume[["date","volume"]]

pre_dataset = dict()

volumes = []
prices = []

# Compute daily stock change (delta = close - open)
post_dates = wsb_daily_volume["date"].tolist()
for post_date in post_dates:
    volume = wsb_daily_volume[wsb_daily_volume["date"].isin([post_date])]["volume"].tolist()
    post_date = post_date[1:len(post_date)-1]
    pre_dataset[post_date] = (volume[0], None)

post_dates = stock_prices["Date"].tolist()
for post_date in post_dates:
    post_date_ymd = utils.mdy_to_ymd(post_date, "/", "-")
    try:
        data_point = pre_dataset[post_date_ymd]
        stock_price = stock_prices[stock_prices["Date"].isin([post_date])]
        volume = list(data_point)[0]
        price = stock_price["Close"].tolist()[0]
        if volume is not None and price is not None:
            prices.append(price)
            volumes.append(volume)
    except KeyError:
        continue # no wallstreetbets volume measurement

X = np.array(prices)
Y = np.array(volumes)

corr1, pvalue1 = scipy.stats.pearsonr(X, Y)
corr2, pvalue2 = scipy.stats.spearmanr(X, Y)
corr3, pvalue3 = scipy.stats.kendalltau(X, Y)

print(corr1)
print(corr2)
print(corr3)

# Conclusion: The correlation is weaker than in saga4
# Like saga4, it probably would have been more significant in January, since the stocks seem to have leveled out more
