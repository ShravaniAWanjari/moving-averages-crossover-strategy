import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

def is_valid_ticker(ticker):
    try:
        test_data = yf.Ticker(ticker).history(period="1d")
        return not test_data.empty
    except Exception:
        return False

st.title("Apply Moving Average Crossover Strategy")

ticker = st.text_input("Enter Ticker Symbol", "MSFT").upper()

yesterday = datetime.now() - timedelta(days=1)
start_date = st.date_input("Select Start Date: (first stock record date: 12th March 1986)",
                           datetime(2013, 1, 1).date(),
                           min_value=datetime(1986, 3, 12).date(),
                           max_value=yesterday.date())
end_date = st.date_input("Select End Date:", yesterday.date(),
                         min_value=datetime(1986, 3, 12).date(),
                         max_value=yesterday.date())

if st.button("Apply Strategy"):

    if not is_valid_ticker(ticker):
        st.error("Invalid ticker symbol. Please enter a valid stock ticker.")
        st.markdown("[Find valid tickers here](https://stockanalysis.com/stocks/)", unsafe_allow_html=True)
        st.stop()

    data = yf.download(ticker, start=start_date, end=end_date)

    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    # EMA Crossover Signals
    data['Signal_EMA'] = np.where(data['EMA50'] > data['EMA200'], 1, 0)
    data['Position_EMA'] = data['Signal_EMA'].diff()

    # SMA Crossover Signals
    data['Signal_SMA'] = np.where(data['SMA50'] > data['SMA200'], 1, 0)
    data['Position_SMA'] = data['Signal_SMA'].diff()

    # Function to plot crossover strategy
    def plot_crossover(data, ma1, ma2, position_col, title, ma1_label, ma2_label):
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(data['Close'], label='Close', color='lightblue', alpha=0.5)
        ax.plot(data[ma2], label=ma2_label, color='green')
        ax.plot(data[ma1], label=ma1_label, color='red')

        # Plot Buy and Sell signals
        ax.plot(data[data[position_col] == 1].index, data[ma1][data[position_col] == 1],
                '^', markersize=10, color='g', label='Buy', alpha=1)
        ax.plot(data[data[position_col] == -1].index, data[ma1][data[position_col] == -1],
                'v', markersize=10, color='r', label='Sell', alpha=1)

        ax.set_title(title, fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Close Price (Log Scale)', fontsize=12)
        ax.set_yscale('log')
        ax.legend()
        ax.grid()
        st.pyplot(fig)

    plot_crossover(data, 'EMA50', 'EMA200', 'Position_EMA', 'EMA Crossover Strategy', '50-day EMA', '200-day EMA')
    plot_crossover(data, 'SMA50', 'SMA200', 'Position_SMA', 'SMA Crossover Strategy', '50-day SMA', '200-day SMA')

    # Calculate Returns
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

    # Plot Cumulative Returns
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(data['Cumulative_Return_SMA'], label='Returns-SMA', color='red', alpha=0.8)
    ax.plot(data['Cumulative_Return_EMA'], label='Returns-EMA', color='green', alpha=0.8)

    ax.set_title('Backtesting EMA and SMA', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Returns (Log Scale)', fontsize=12)
    ax.set_yscale('log')
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # Display Trade Signals
    results_table = data[data['Position_EMA'].isin([1, -1])][['Close', 'Position_EMA']].copy()
    results_table['Position_EMA'] = results_table['Position_EMA'].replace({1: 'Buy', -1: 'Sell'})

    st.subheader("Trade Signals Table")
    st.dataframe(results_table, use_container_width=True)