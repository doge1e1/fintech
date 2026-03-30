def myStrategy(pastPriceVec, currentPrice):
    import numpy as np
    import pandas as pd
    windowSize=11
    alpha=-1
    beta=-4
    action = 0  # action=1(buy), -1(sell), 0(hold), with 0 as the default action

    dataLen = len(pastPriceVec)  # Length of the data vector
    if dataLen < windowSize + 1:
        return action  # Not enough data to calculate RSI or MA

    # Convert past prices to a pandas Series
    price_series = pd.Series(pastPriceVec)

    # Calculate Moving Average (MA)
    if dataLen < windowSize:
        ma = price_series.mean()  # If given price vector is smaller than windowSize, use the average
    else:
        ma = price_series.rolling(window=windowSize).mean().iloc[-1]  # Normal moving average

    # Calculate RSI
    delta = price_series.diff()

    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate the average gain and loss
    avg_gain = gain.rolling(window=windowSize).mean().iloc[-1]
    avg_loss = loss.rolling(window=windowSize).mean().iloc[-1]

    # Avoid division by zero
    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # Determine action based on RSI value and MA
    # Buy signal: RSI < (30 + alpha) and current price > MA (indicating an uptrend)
    if rsi < (30 + alpha) and currentPrice > ma:
        action = 1  # Buy

    # Sell signal: RSI > (70 - beta) and current price < MA (indicating a downtrend)
    elif rsi > (70 - beta) and currentPrice < ma:
        action = -1  # Sell

    return action
