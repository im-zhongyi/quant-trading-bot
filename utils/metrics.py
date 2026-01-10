import numpy as np

def sharpe_ratio(returns, risk_free_rate=0):
    if returns.std() == 0:
        return 0
    return (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)

def max_drawdown(equity_curve):
    cum_max = equity_curve.cummax()
    drawdown = (equity_curve - cum_max) / cum_max
    return drawdown.min()
