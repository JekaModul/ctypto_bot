from ta.volatility import BollingerBands

def calculate_bollinger_bands(data, window=20, window_dev=2):
    indicator_bb = BollingerBands(close=data['close'], window=window, window_dev=window_dev)
    data['bb_hband'] = indicator_bb.bollinger_hband()
    data['bb_lband'] = indicator_bb.bollinger_lband()
    return data

