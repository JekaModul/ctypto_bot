from utils.data_fetch import fetch_ohlcv
from indicators.rsi_indicator import calculate_rsi
from indicators.bollinger_bands_indicator import calculate_bollinger_bands
from indicators.macd_indicator import calculate_macd
from datetime import datetime
from bot.telegram_bot import send_telegram_message
from utils.ml_model import predict_price


async def analyze_symbol(symbol, exchange, current_states, model, scaler):
    try:
        look_back = 200
        candles = fetch_ohlcv(exchange, symbol)
        candles = calculate_rsi(candles)
        candles = calculate_bollinger_bands(candles)
        candles = calculate_macd(candles)
        new_state = None  # Переменная для нового состояния
        current_price = candles['close'].iloc[-1]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        last_sequence = candles['close'].values[-look_back:].reshape(-1, 1)
        last_sequence_scaled = scaler.transform(last_sequence)
        predicted_price = predict_price(model, scaler, last_sequence_scaled)

        print(f"Analyzing {symbol} at {current_time}")
        print(f"Current price: {current_price} USDT")
        print(f"Predicted price: {predicted_price} USDT")

        if (predicted_price < current_price and candles['macd_line'].iloc[-1] > candles['macd_signal'].iloc[-1]
                and candles['rsi'].iloc[-1] > 70 and candles['close'].iloc[-1] > candles['bb_hband'].iloc[-1]):
            new_state = 'sell'
            message = (f"Актив <i>{symbol}</i> \n\nЦена вышла за верхнюю полосу Боллинджера, "
                       f"RSI указывает на перекупленность, MACD-линия пересекла сигнальную линию вверх. "
                       f"\n\n<b>Прогнозируемая цена: {predicted_price} USDT</b>."
                       f"\n\n<b>Текущая цена: {current_price} USDT</b>. \n\nВремя: {current_time}")

        elif (predicted_price > current_price and candles['macd_line'].iloc[-1] < candles['macd_signal'].iloc[-1]
              and candles['rsi'].iloc[-1] < 30 and candles['close'].iloc[-1] < candles['bb_lband'].iloc[-1]):
            new_state = 'buy'
            message = (f"Актив <i>{symbol}</i> \n\nЦена вышла за нижнюю полосу Боллинджера, "
                       f"RSI указывает на перепроданность, MACD-линия пересекла сигнальную линию вниз. "
                       f"\n\n<b>Прогнозируемая цена: {predicted_price} USDT</b>."
                       f"\n\n<b>Текущая цена: {current_price} USDT</b>. \n\nВремя: {current_time}")

        # Если состояние изменилось, отправляем сообщение
        if new_state != current_states[symbol]:
            current_states[symbol] = new_state
            await send_telegram_message(message)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
