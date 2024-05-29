from ta.momentum import RSIIndicator

def calculate_rsi(data, window=14):
    rsi_indicator = RSIIndicator(close=data['close'], window=window)
    data['rsi'] = rsi_indicator.rsi()
    return data

