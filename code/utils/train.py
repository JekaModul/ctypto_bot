import ccxt
from data_fetch import fetch_ohlcv
from ml_model import train_model, save_model
import pickle

# Инициализация биржи
exchange = ccxt.okx()

# Список активов
symbols = ['BTC/USDT', 'ETH/USDT', 'NEAR/USDT', 'BNB/USDT', 'XRP/USDT', 'TRB/USDT']

for symbol in symbols:
    # Получение исторических данных
    print(f"Fetching data for {symbol}...")
    data = fetch_ohlcv(exchange, symbol)

    # Обучение модели
    print(f"Training model for {symbol}...")
    model, scaler = train_model(data['close'].values.reshape(-1, 1))

    # Сохранение модели и scaler
    print(f"Saving model and scaler for {symbol}...")
    model_path = f"models/{symbol.replace('/', '_')}_model.h5"
    scaler_path = f"models/{symbol.replace('/', '_')}_scaler.pkl"
    save_model(model, model_path)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

    print(f"Done with {symbol}!")
