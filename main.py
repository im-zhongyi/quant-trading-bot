import argparse
from backtests.run_backtest import run_backtest
from backtests.run_bulk_backtests import run_bulk_backtests
from utils.config import get_config_filepath


def main():
    parser = argparse.ArgumentParser(
        description="Quant Trading Backtest Runner"
    )

    subparsers = parser.add_subparsers(
        dest="mode",
        required=True
    )

    # ---------- SINGLE BACKTEST ----------
    single_parser = subparsers.add_parser(
        "single",
        help="Run a single backtest"
    )

    single_parser.add_argument(
        "--symbol",
        type=str,
        default="BTC/USDT",
        help="Trading pair, e.g. BTC/USDT"
    )

    single_parser.add_argument(
        "--timeframe",
        type=str,
        default="4h",
        help="Candle timeframe, e.g. 15m, 1h"
    )

    single_parser.add_argument(
        "--limit",
        type=int,
        default=5000,
        help="Number of candles"
    )

    single_parser.add_argument(
        "--risk",
        type=int,
        default=2,
        help="Risk per trade as a percentage (e.g. 2 for 2%)"
    )


    single_parser.add_argument(
        "--stoploss",
        type=int,
        default=5,
        help="Stop loss as a percentage (e.g. 2 for 2%)"
    )


    # ---------- BULK BACKTEST ----------
    bulk_parser =subparsers.add_parser(
        "bulk",
        help="Run bulk backtests"
    )

    bulk_parser.add_argument(
        "--config",
        type=str,
        default="bulk_backtest",
        help="Path to bulk backtest config YAML"
    )
    args = parser.parse_args()

    # ---------- ROUTING ----------
    if args.mode == "single":
        print("▶ Running SINGLE backtest")
        run_backtest(
            symbol=args.symbol,
            timeframe=args.timeframe,
            limit=args.limit,
            risk_per_trade=args.risk / 100,
            stop_loss_pct=args.stoploss / 100
        )

    elif args.mode == "bulk":
        filename = get_config_filepath(args.config)
        print("🚀 Running BULK backtests")
        run_bulk_backtests(filename)


if __name__ == "__main__":
    main()
