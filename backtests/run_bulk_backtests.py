from backtests.run_backtest import run_backtest
from utils.config import load_yaml
from utils.dates import generate_timestamp
import time
import os
import pandas as pd
from itertools import product

# default config path: "config/bulk_backtest.yaml"
def run_bulk_backtests(config_path="config/bulk_backtest.yaml"):
    config = load_yaml(config_path)
    combinations = product(
        config["symbols"],
        config["timeframes"],
        config["limits"],
        config["risk_per_trade"],
        config["stop_loss_pct"],
        
    ) 
    summary_rows = []
    # total = len(config["symbols"]) * len(config["timeframes"]) * len(config["limits"]) * len(config["risk_per_trade"]) * len(config["stop_loss_pct"])
    for n, (symbol, timeframe, limit, risk_per_trade, stop_loss_pct) in enumerate(combinations,1):
        print(
            f"Running backtest: {symbol} | {timeframe} | {limit}"
        )

        try:
            # print(f"Progress: {n}/{total} runs completed", end="\r", flush=True)
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
                "max_drawdown": metrics["max_drawdown"],
                "profit_margin": str((metrics["final_capital"]/config["initial_capital"] - 1) *100 )+"%"
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
