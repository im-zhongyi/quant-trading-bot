from backtests.run_backtest import run_backtest
from utils.dates import generate_timestamp
import time
import os
import pandas as pd

SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "ADA/USDT",
    "SOL/USDT",
]

TIMEFRAMES = [
    "15m",
    "1h",
    "4h"
]

LIMITS = [
    2000,
    5000
]

RISK_PER_TRADE = [
    0.05, 
    0.04, 
    0.03
]

STOP_LOSS_PCT = [
    0.10,
    0.07,
    0.05
]
def run_bulk_backtests():
    summary_rows = []

    for symbol in SYMBOLS:
        for timeframe in TIMEFRAMES:
            for limit in LIMITS:
                for risk_per_trade in RISK_PER_TRADE:
                    for stop_loss_pct in STOP_LOSS_PCT:
                        print(
                            f"Running backtest: {symbol} | {timeframe} | {limit}"
                        )

                        try:
                            metrics = run_backtest(
                                symbol=symbol,
                                timeframe=timeframe,
                                limit=limit,
                                risk_per_trade=risk_per_trade,
                                stop_loss_pct=stop_loss_pct,
                                return_metrics=True
                            )

                        
                            summary_rows.append({
                                "symbol": symbol,
                                "timeframe": timeframe,
                                "candles": metrics["limit"],
                                "risk_per_trade": risk_per_trade,
                                "stop_loss_pct": stop_loss_pct,
                                "final_capital": metrics["final_capital"],
                                "sharpe": metrics["sharpe"],
                                "max_drawdown": metrics["max_drawdown"]
                            })
                            time.sleep(1.2)
                        except Exception as e:
                            print(
                                f"❌ Failed: {symbol} {timeframe} {limit} → {e}"
                            )
    # -------------------
    # SAVE SUMMARY CSV
    # -------------------
    os.makedirs(f"data/processed/summary", exist_ok=True)
    summary_df = pd.DataFrame(summary_rows)

    ts = generate_timestamp()
    summary_path = f"data/processed/summary/bulk_results_{ts}.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\n✅ Summary saved to {summary_path}")
