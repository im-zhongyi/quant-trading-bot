def calculate_position_size(
    capital,
    risk_per_trade,
    entry_price,
    stop_loss_pct
):
    risk_amount = capital * risk_per_trade
    stop_loss_price = entry_price * (1 - stop_loss_pct)
    risk_per_unit = entry_price - stop_loss_price

    if risk_per_unit <= 0:
        return 0

    return risk_amount / risk_per_unit
