# Moving Average Crossover Strategy

## Overview

This project implements the Moving Average Crossover strategy for algorithmic trading. The strategy utilizes short-term and long-term moving averages to generate buy and sell signals for a given financial instrument.

## Features

- Implements Simple Moving Averages (SMA) and Exponential Moving Averages (EMA) for trading signals
- Backtesting on historical data
- Visualization of moving averages and trade signals
- Performance evaluation using key metrics

## Dataset

The strategy is tested on historical market data provided in `Data.csv`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/moving-average-crossover.git
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
<img src="images/Close%20Price%20graph.png" alt="Close Price Graph" width="400"/>

### SMA 50 vs SMA 200
<img src="images/SMA50_SM200.png" alt="SMA 50 vs SMA 200" width="400"/>

### Simple Moving Average (SMA) Signals
<img src="images/SMA_signals.png" alt="SMA Signals" width="400"/>

### EMA 50 vs EMA 200
<img src="images/EMA50_EMA200.png" alt="EMA 50 vs EMA 200" width="400"/>

### Exponential Moving Average (EMA) Signals
<img src="images/EMA_signals.png" alt="EMA Signals" width="400"/>

## Returns and Final Results

Based on the cumulative returns graph, the Exponential Moving Average (EMA) strategy outperformed the Simple Moving Average (SMA) strategy.

- **Total Return SMA**: 282.27%
- **Total Return EMA**: 287.61%

<img src="images/returns_comparison.png" alt="Returns Comparison" width="600"/>

## Future Improvements

- Implementing more sophisticated trading strategies
- Adding risk management features
- Backtesting with different timeframes
- Enhancing performance evaluation

## Contributing

Contributions are welcome! Feel free to fork the repo, create a branch, and submit a pull request.

## License

This project is licensed under the MIT License.