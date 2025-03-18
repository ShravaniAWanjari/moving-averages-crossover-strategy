import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

st.title("EMA Crossover Strategy")

yesterday = datetime.now() - timedelta(days=1)

ticker = st.text_input("Enter Ticker Symbol:", "AAPL")
start_date = st.date_input("Select Start Date:", datetime(2020, 1, 1).date(), min_value=datetime(1986, 3, 13).date(), max_value=yesterday.date())
end_date = st.date_input("Select End Date:", yesterday.date(), min_value=datetime(1986, 3, 13).date(), max_value=yesterday.date())

if st.button("Apply Strategy"):
    data = yf.download(ticker, start=start_date, end=end_date)

    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    

    data['Signal_EMA'] = 0  
    data['Signal_EMA'] = np.where(data['EMA50'] > data['EMA200'], 1, 0) 

    data['Signal_SMA'] = 0  
    data['Signal_SMA'] = np.where(data['SMA50'] > data['SMA200'], 1, 0) 

    data['Position_EMA'] = data['Signal_EMA'].diff()
    data['Position_SMA'] = data['Signal_SMA'].diff()
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(data['Close'], label='Close', color='lightblue', alpha=0.5)
    ax.plot(data['EMA200'], label='200-day EMA', color='green')
    ax.plot(data['EMA50'], label='50-day EMA', color='red')

    ax.plot(data[data['Position_EMA'] == 1].index, data['EMA50'][data['Position_EMA'] == 1], '^', markersize=10, color='g', label='Buy', alpha=1)
    ax.plot(data[data['Position_EMA'] == -1].index, data['EMA50'][data['Position_EMA'] == -1], 'v', markersize=10, color='r', label='Sell', alpha=1)

    ax.set_title('EMA Crossover Strategy', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Close', fontsize=12)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

        # Plotting SMA Crossover
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(data['Close'], label='Close', color='lightblue', alpha=0.5)
    ax.plot(data['SMA200'], label='200-day SMA', color='green')
    ax.plot(data['SMA50'], label='50-day SMA', color='red')

    # Plot buy signals for SMA
    ax.plot(data[data['Position_SMA'] == 1].index, data['SMA50'][data['Position_SMA'] == 1], '^', markersize=10, color='g', label='Buy', alpha=1)
    # Plot sell signals for SMA
    ax.plot(data[data['Position_SMA'] == -1].index, data['SMA50'][data['Position_SMA'] == -1], 'v', markersize=10, color='r', label='Sell', alpha=1)

    # Add labels and title for SMA
    ax.set_title('SMA Crossover Strategy', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Close', fontsize=12)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    st.divider()


    data['Daily_Return'] = data['Close'].pct_change()

    data['Strategy_Return_SMA'] = data['Daily_Return'] * data['Signal_SMA'].shift(1)
    data['Strategy_Return_EMA'] = data['Daily_Return'] * data['Signal_EMA'].shift(1)

    data['Cumulative_Return_SMA'] = (1 + data['Strategy_Return_SMA']).cumprod()
    data['Cumulative_Return_EMA'] = (1 + data['Strategy_Return_EMA']).cumprod()

    total_return_sma = data['Cumulative_Return_SMA'].iloc[-1] - 1
    total_return_ema = data['Cumulative_Return_EMA'].iloc[-1] - 1
    
    st.subheader("Returns:")
    st.write(f"**EMA:** {total_return_ema:.2%}")
    st.write(f"**SMA:** {total_return_sma:.2%}")
    # Comparison Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(data['Cumulative_Return_SMA'], label='Returns-SMA', color='red', alpha=0.8)
    ax.plot(data['Cumulative_Return_EMA'], label='Returns-EMA', color='green', alpha=0.8)

    ax.set_title('Backtesting EMA and SMA', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Close', fontsize=12)
    ax.legend()
    ax.grid()
    st.pyplot(fig)