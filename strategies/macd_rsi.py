import pandas_ta as ta

def apply_indicators(df, config):
    rsi_cfg = config["rsi"]
    macd_cfg = config["macd"]

    df["rsi"] = ta.rsi(df["close"], length=rsi_cfg["length"])

    macd = ta.macd(
        df["close"],
        fast=macd_cfg["fast"],
        slow=macd_cfg["slow"],
        signal=macd_cfg["signal"],
    )
    df = df.join(macd)

    return df


def generate_signals(df, config):
    df["signal"] = 0

    macd_col = "MACD_12_26_9"
    signal_col = "MACDs_12_26_9"

    bullish_cross = (
        (df[macd_col].shift(1) <= df[signal_col].shift(1)) &
        (df[macd_col] > df[signal_col])
    )

    bearish_cross = (
        (df[macd_col].shift(1) >= df[signal_col].shift(1)) &
        (df[macd_col] < df[signal_col])
    )

    df.loc[
        bullish_cross & (df["rsi"] < 40),
        "signal"
    ] = 1

    df.loc[
        bearish_cross & (df["rsi"] > 60),
        "signal"
    ] = -1

    return df

