# Quant Trading Bot

A Python-based **quantitative trading backtesting framework** for stocks and crypto.  
This project supports **single backtests**, **bulk backtests**, and **trade logging** with MACD + RSI strategy.

---

## Features

- **Single backtest** for one symbol, timeframe, and candle count
- **Bulk backtests** across multiple symbols, timeframes, and candle lengths
- Logs all trades in CSV with informative filenames
- Generates **summary CSV** with metrics: `final capital`, `Sharpe ratio`, `max drawdown`
- Easy-to-extend to other strategies and indicators
- Configurable timeframe, candle limit, and symbols
- Supports both **crypto (e.g., BTC/USDT)** and stock backtesting

---

## Folder Structure

```text
quant-trading-bot/
├── backtests/
│   ├── __init__.py
│   ├── run_backtest.py
│   └── run_bulk_backtests.py
├── data/
│   ├── processed/
│   │   ├── trades/
│   │   └── summary/
├── main.py
└── README.md
```
---

## Installation

### Clone the repo:

> git clone https://github.com/yourusername/quant-trading-bot.git
> cd quant-trading-bot


### Install dependencies:

> pip install -r requirements.txt


Dependencies might include: pandas, numpy, matplotlib, ccxt (for crypto data), etc.

---

## Usage
### Single Backtest

Run a single backtest for a specific symbol:

> python main.py single BTC/USDT 15m 5000


BTC/USDT → symbol

15m → timeframe

5000 → number of candles to fetch

Trades will be saved to:

> data/processed/trades/trades_BTC_USDT_15m_5000_<timestamp>.csv

### Bulk Backtests

Run multiple backtests at once:

> python main.py bulk

Runs all combinations of SYMBOLS, TIMEFRAMES, LIMITS defined in run_bulk_backtests.py

Generates summary CSV:

> data/processed/summary/bulk_results_<timestamp>.csv

### Trade Logging & Metrics

Trades CSV:
Logs each individual trade with timestamp, price, side, and PnL.
Filename format:
> trades_<SYMBOL>_<TIMEFRAME>_<CANDLES>_<TIMESTAMP>.csv

Summary CSV:
Aggregates metrics for each backtest:
```text
symbol	timeframe	candles	final_capital	sharpe	max_drawdown
BTC_USDT	15m	5000	9192.21	-0.12	-14.8
```

### Customization

Symbols: Modify SYMBOLS list in run_bulk_backtests.py
Timeframes: Modify TIMEFRAMES list
Candle Limits: Modify LIMITS list
Strategy: Currently MACD + RSI — you can extend or replace logic in run_backtest.py
Return metrics: Optional flag return_metrics allows capturing results in bulk tests

--- 

## Notes

Filenames are sanitized for filesystem compatibility (BTC/USDT → BTC_USDT)
Trades and summary CSVs are timestamped for reproducibility
Bulk tests are O(n1n2n3); consider parallel execution for faster runs
Ensure you run scripts from the project root:

> python main.py ...

## Future Improvements
<ul>
    <li>Add parameter sweep for MACD / RSI</li>
    <li>Add equity curve plots</li>
    <li>Integrate with live exchange data</li>
    <li>Add config files (YAML/JSON) to define experiments</li>
    <li>Parallelize bulk backtests to reduce runtime</li>
</ul>

## License
MIT License