from ta.trend import MACD

def calculate_macd(data, window_slow=26, window_fast=12, window_sign=9):
    macd_indicator = MACD(close=data['close'], window_slow=window_slow,
                          window_fast=window_fast, window_sign=window_sign)
    data['macd_line'] = macd_indicator.macd()
    data['macd_signal'] = macd_indicator.macd_signal()
    data['macd_diff'] = macd_indicator.macd_diff()
    return data


