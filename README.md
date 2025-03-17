# Moving Average Crossover Strategy

## Overview

This project implements the Moving Average Crossover strategy for algorithmic trading. The strategy utilizes short-term and long-term moving averages to generate buy and sell signals for a given asset.

## Golden Cross Strategy

##### The Golden Cross occurs when a shorter moving average crosses above a longer one, signaling a bullish trend:
- SMA Golden Cross: When the SMA50 crosses above the SMA200, it indicates a potential long entry.
- EMA Golden Cross: The same concept applies to EMAs, which provide quicker signals due to their responsiveness to recent price action.

## Features

- Implements Simple Moving Averages (SMA) and Exponential Moving Averages (EMA) for trading signals
- Visualization of moving averages and trade signals
- Performance evaluation using cumulative returns for EMA and SMA

## Dataset

The strategy is tested on historical market data of Microsoft (MSFT) using **yfinance**.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShravaniAWanjari/moving-average-crossover.git
   cd moving-average-crossover
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Jupyter Notebook to execute the strategy:

```bash
jupyter notebook code.ipynb
```

## Strategy Explanation

1. **Short-Term SMA**: Calculates a fast-moving average (e.g., 50-day SMA)
2. **Long-Term SMA**: Calculates a slow-moving average (e.g., 200-day SMA)
3. **Buy Signal**: When the short-term SMA crosses above the long-term SMA
4. **Sell Signal**: When the short-term SMA crosses below the long-term SMA

## Outcomes & Visual Insights

### Close Price Graph
<img src="images/Close%20Price%20graph.png" alt="Close Price Graph" width="500"/>

### SMA 50 vs SMA 200
<img src="images/SMA50_SM200.png" alt="SMA 50 vs SMA 200" width="500"/>

### Simple Moving Average (SMA) Signals
<img src="images/SMA_signals.png" alt="SMA Signals" width="500"/>

### EMA 50 vs EMA 200
<img src="images/EMA50_EMA200.png" alt="EMA 50 vs EMA 200" width="500"/>

### Exponential Moving Average (EMA) Signals
<img src="images/EMA_signals.png" alt="EMA Signals" width="500"/>

## Returns and Final Results

Based on the cumulative returns graph, EMA performed better than SMA.

- Total Return SMA: **282.27%**
- Total Return EMA: **287.61%**

<img src="images/returns_comparison.png" alt="Returns Comparison" width="600"/>

## Future Improvements

- Building a streamlit application to include user intput asset tickers, that way anyone can use it to get quick insights on the asset's performance
- Going further on incorporating trading methodologies
- Adding risk management features
- Training an ML model for the same objective and drawing a comparison.

## Contributing

Contributions are welcome! Feel free to fork the repo, create a branch, and submit a pull request.
