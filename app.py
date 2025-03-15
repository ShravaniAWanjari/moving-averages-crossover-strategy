import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


st.title("Analyze Moving Average Crossover Strategy")

ticker = st.text_input("Enter Ticker Symbol", "APPL").upper()

if not ticker.isalpha():
    st.error("Invalid ticker symbol. Please enter a valid stock ticker.")
    st.markdown("<a href='https://stockanalysis.com/stocks/'>Oops</a>!", unsafe_allow_html=True)
    st.stop()

yesterday = datetime.now() - timedelta(days=1)
start_date = st.date_input("Select Start Date:", datetime(2023, 1, 1).date(), min_value=datetime(1986, 3, 13).date(), max_value=yesterday.date())
end_date = st.date_input("Select End Date:", datetime(2024, 1, 1).date(), min_value=datetime(1986, 3, 13).date(), max_value=yesterday.date())

if end_date < start_date:
    st.error("Error: End date cannot be earlier than start date. Please select a valid date range.")
else:
    st.success(f"Analyzing {ticker}")


df = yf.download(ticker, start=start_date, end=end_date)

df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()
df['EMA_50'] = df['Close'].ewm(span=50).mean()
df['EMA_200'] = df['Close'].ewm(span=200).mean()


def plot_sma_crossover():
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'], label='Close Price', alpha=0.7)
    ax.plot(df.index, df['SMA_50'], label='SMA 50', linestyle='dashed')
    ax.plot(df.index, df['SMA_200'], label='SMA 200', linestyle='dashed')
    ax.set_title("SMA Crossover Strategy")
    ax.legend()
    st.pyplot(fig)

def plot_ema_crossover():
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'], label='Close Price', alpha=0.7)
    ax.plot(df.index, df['EMA_50'], label='EMA 50', linestyle='dashed')
    ax.plot(df.index, df['EMA_200'], label='EMA 200', linestyle='dashed')
    ax.set_title("EMA Crossover Strategy")
    ax.legend()
    st.pyplot(fig)

df['Daily Returns'] = df['Close'].pct_change()
df['Cumulative Returns'] = (1 + df['Daily Returns']).cumprod()

def plot_cumulative_returns():
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Cumulative Returns'], label='Cumulative Returns', color='green')
    ax.set_title("Cumulative Returns")
    ax.legend()
    st.pyplot(fig)

df['Signal'] = 0
df['Signal'][df['SMA_50'] > df['SMA_200']] = 1  # Buy signal
df['Signal'][df['SMA_50'] < df['SMA_200']] = -1  # Sell signal

df['Buy'] = (df['Signal'] == 1) & (df['Signal'].shift(1) == 0)
df['Sell'] = (df['Signal'] == -1) & (df['Signal'].shift(1) == 0)

fig, ax = plt.subplots()
ax.plot(df.index, df['Close'], label='Close Price', alpha=0.7)
ax.plot(df.index, df['SMA_50'], label='SMA 50', linestyle='dashed')
ax.plot(df.index, df['SMA_200'], label='SMA 200', linestyle='dashed')
ax.set_title("SMA Crossover Strategy")
ax.legend()
####need to fix the position logic here
ax.plot(df[df['Buy'].index], df['Close'][df['Buy']], '^', markersize=10, color='g', label='Buy', alpha=1)

ax.plot(df[df['Sell'].index], df['Close'][df['Sell']], 'v', markersize=10, color='r', label='Sell', alpha=1)

st.pyplot(fig)

plot_sma_crossover()
plot_ema_crossover()
plot_cumulative_returns()

