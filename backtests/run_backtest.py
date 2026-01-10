import os
import pandas as pd
import ccxt
import yaml
from strategies.macd_rsi import apply_indicators, generate_signals
from utils.metrics import sharpe_ratio, max_drawdown
from utils.dates import generate_timestamp
INITIAL_CAPITAL = 10_000
FEE_RATE = 0.01  # 0.1%
# define stop loss percentage
STOP_LOSS_PCT = 0.02
RISK_PER_TRADE = 0.01



def fetch_data(symbol, timeframe, limit):
    exchange = ccxt.binance()
    all_bars = []

    timeframe_ms = exchange.parse_timeframe(timeframe) * 1000
    since = exchange.milliseconds() - limit * timeframe_ms

    while True:
        bars = exchange.fetch_ohlcv(
            symbol,
            timeframe=timeframe,
            since=since,
            limit=1000
        )

        if not bars:
            break

        all_bars.extend(bars)

        since = bars[-1][0] + timeframe_ms

        if len(all_bars) >= limit:
            break

    df = pd.DataFrame(
        all_bars[:limit],
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    print (f"Fetched {len(df)} bars for {symbol} at {timeframe} timeframe.")
    return df


def run_backtest(
    symbol="ADA/USDT",
    timeframe="4h", # 1m, 5m, 15m, 30m, 1h, 4h, 1d
    limit=10000,
    return_metrics=False
):
    with open("config/strategy.yaml") as f:
        strategy_config = yaml.safe_load(f)

    df = fetch_data(symbol, timeframe, limit)
    df = apply_indicators(df, strategy_config)
    df = generate_signals(df, strategy_config)
    df.dropna(inplace=True)

    capital = INITIAL_CAPITAL
    position = 0
    entry_price = 0
    equity_curve = []
    trades = []
    current_trade = None
    for i in range(1, len(df)):
        row = df.iloc[i]
        price = row["close"]
        signal = row["signal"]
        timestamp = row["timestamp"]

        # EXIT
        if position > 0:
            stop_loss_hit = price <= entry_price * (1 - STOP_LOSS_PCT)
            signal_exit = signal == -1

            if stop_loss_hit or signal_exit:
                exit_price = price
                exit_reason = "STOP_LOSS" if stop_loss_hit else "SIGNAL"
 
                capital += position * exit_price * (1 - FEE_RATE)

                pnl = (exit_price - entry_price) * position
                pnl_pct = (exit_price - entry_price) / entry_price * 100

                current_trade.update({
                    "exit_time": timestamp,
                    "exit_price": round(exit_price, 4),
                    "pnl": round(pnl, 2),
                    "pnl_pct": round(pnl_pct, 2),
                    "exit_reason": exit_reason,
                })

                trades.append(current_trade)

                position = 0
                entry_price = 0
                current_trade = None

        # ENTRY
        if position == 0 and signal == 1:
            position = (capital * RISK_PER_TRADE) / (price * STOP_LOSS_PCT)
            position = min(position, capital / price)

            entry_price = price
            capital -= position * price * (1 + FEE_RATE)

            current_trade = {
                "entry_time": timestamp,
                "side": "LONG",
                "entry_price": round(entry_price, 4),
                "position_size": round(position, 6),
            }
        equity_curve.append(capital + position * price)



    equity_curve = pd.Series(equity_curve)
    returns = equity_curve.pct_change().dropna()
    # Format trade log filename
    current_timestamp = generate_timestamp()
    sanitized_symbol = symbol.replace("/", "_")
    # Create folder base on symbol
    os.makedirs(f"data/processed/{sanitized_symbol}", exist_ok=True)
    trade_filename = (
        f"trades_{sanitized_symbol}_{timeframe}_{len(df)}_{current_timestamp}.csv"
    )
    trade_log_path = f"data/processed/{sanitized_symbol}/{trade_filename}"
    
    trades_df = pd.DataFrame(trades)
    trades_df.to_csv(trade_log_path, index=False)


    # print summary for each backtest run
    print(f"Trades saved to {trade_log_path}")
    print(f"Total trades: {len(trades_df)}")
    print("Total BUY signals:", (df["signal"] == 1).sum())
    print("Total SELL signals:", (df["signal"] == -1).sum())
    print("Final Capital:", round(equity_curve.iloc[-1], 2))
    print("Sharpe Ratio:", round(sharpe_ratio(returns), 2))
    print("Max Drawdown:", round(max_drawdown(equity_curve) * 100, 2), "%")
    if return_metrics:
        return {
            "final_capital": round(equity_curve.iloc[-1], 2),
            "sharpe": round(sharpe_ratio(returns), 2),
            "max_drawdown": round(max_drawdown(equity_curve) * 100, 2)
        }

if __name__ == "__main__":
    run_backtest()
