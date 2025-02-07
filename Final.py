import numpy as np
import pandas as pd
from jugaad_data.nse import stock_df
import matplotlib as plt
from datetime import date

df = stock_df(symbol = "SBIN", series="EQ", from_date=date(2015, 12, 1), to_date=date(2025, 1, 31))
df = df[['DATE', 'CLOSE']]
df.rename(columns={'DATE': 'Date', 'CLOSE': 'Closing Price'}, inplace = True)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace = True)

df = df.resample('M').last()

initial_capital = 10000
fd_rate_monthly = 8/12/100

capital = initial_capital
fd_balance = initial_capital
stocks = 0
signal = 0
total_investment = []

data = []

for i in range(len(df)):
    current_price = df.iloc[i]['Closing Price']
    fd_balance *= (1 + fd_rate_monthly)
    if current_price < fd_balance:
        stocks += 2
        capital -= 2 * current_price
        signal = 0
    else:
        signal += 1

    if signal == 3:
        capital += initial_capital + current_price
        total_investment.append(stocks)
        stocks = 0
        signal = 0
    
    data.append({'Date': df.index[i],
                 'FD Balance': fd_balance,
                 'Cash Price': current_price,
                 'Capital': capital,
                 'Stocks': stocks})
    
if stocks > 0:
    capital += stocks * df.iloc[i]['Closing Price']
    total_investment.append(stocks)

results = pd.DataFrame(data)

final_balance = capital + fd_balance
absolute_return = final_balance - initial_capital

returns = results['Capital'].pct_change().dropna()
sharpe_ratio = returns.mean() / returns.std() * np.sqrt(12)

print("Final Balance:", final_balance)
print("absolute return:", absolute_return)
print("Sharpe Ratio:", sharpe_ratio)
        
    