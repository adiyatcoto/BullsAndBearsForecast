#!/usr/bin/env python
# coding: utf-8

# In[3]:


import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Fetch GC=F data from Yahoo Finance
symbol = "GC=F"
start_date = "2020-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(symbol, start=start_date, end=end_date, progress=False)

# Calculate daily returns
data['Return'] = data['Close'].pct_change()

# Group data by different timeframes
weekly_data = data.resample('W').agg({'Return': 'sum', 'High': 'max', 'Low': 'min', 'Close': 'last'})
monthly_data = data.resample('M').agg({'Return': 'sum', 'High': 'max', 'Low': 'min', 'Close': 'last'})
quarterly_data = data.resample('Q').agg({'Return': 'sum', 'High': 'max', 'Low': 'min', 'Close': 'last'})
bi_quarterly_data = data.resample('2Q').agg({'Return': 'sum', 'High': 'max', 'Low': 'min', 'Close': 'last'})
yearly_data = data.resample('Y').agg({'Return': 'sum', 'High': 'max', 'Low': 'min', 'Close': 'last'})

timeframes = [('Weekly', weekly_data), ('Monthly', monthly_data), ('Quarterly', quarterly_data), ('Bi-Quarterly', bi_quarterly_data), ('Yearly', yearly_data)]

# Calculate trend imbalance and residual range for each timeframe
for timeframe, timeframe_data in timeframes:
    bear_days = len(timeframe_data[timeframe_data['Return'] < 0])
    bull_days = len(timeframe_data[timeframe_data['Return'] > 0])
    
    total_days = len(timeframe_data)
    bear_percentage = (bear_days / total_days) * 100
    bull_percentage = (bull_days / total_days) * 100
    
    imbalance = abs(bear_percentage - bull_percentage)
    trend_balance = "Bear" if bear_percentage > bull_percentage else "Bull"
    
    print(f"Trend Balance for {timeframe}: {trend_balance} (Imbalance: {imbalance:.2f}%)")
    
    # Calculate residual range for bear and bull periods
    bear_range = timeframe_data.loc[timeframe_data['Return'] < 0, 'High'] - timeframe_data.loc[timeframe_data['Return'] < 0, 'Low']
    bull_range = timeframe_data.loc[timeframe_data['Return'] > 0, 'High'] - timeframe_data.loc[timeframe_data['Return'] > 0, 'Low']
    
    print(f"Residual Range for Bear Days: Mean = {bear_range.mean():.2f}, Max = {bear_range.max():.2f}, Min = {bear_range.min():.2f}")
    print(f"Residual Range for Bull Days: Mean = {bull_range.mean():.2f}, Max = {bull_range.max():.2f}, Min = {bull_range.min():.2f}")
    print("-" * 30)
    
    # Visualize residual range using box plot
    plt.figure(figsize=(8, 6))
    plt.boxplot([bear_range, bull_range], labels=['Bear Days', 'Bull Days'])
    plt.ylabel('Residual Range')
    plt.title(f'{symbol} {timeframe} Residual Range')
    plt.show()

    # Calculate projected price movements based on residual range
    current_price = timeframe_data['Close'].iloc[-1]
    projected_bear_price = current_price - bear_range.mean()
    projected_bull_price = current_price + bull_range.mean()
    
    print(f"Projected Price Movement for Bear Days: {current_price:.2f} - {bear_range.mean():.2f} = {projected_bear_price:.2f}")
    print(f"Projected Price Movement for Bull Days: {current_price:.2f} + {bull_range.mean():.2f} = {projected_bull_price:.2f}")
    print("-" * 30)

