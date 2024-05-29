import asyncio
import ccxt
from bot.telegram_bot import send_telegram_message
from bot.analyze import analyze_symbol
from utils.ml_model import load_model
import pickle

exchange = ccxt.okx()
symbols = ['BTC/USDT', 'ETH/USDT', 'NEAR/USDT', 'BNB/USDT', 'XRP/USDT', 'TRB/USDT']  # Список активов
current_states = {symbol: None for symbol in symbols}  # Словарь для отслеживания состояний каждого актива

# Загрузка моделей и scalers для каждого актива
models = {}
scalers = {}
for symbol in symbols:
    model_path = f"models/{symbol.replace('/', '_')}_model.h5"
    scaler_path = f"models/{symbol.replace('/', '_')}_scaler.pkl"
    models[symbol] = load_model(model_path)
    with open(scaler_path, 'rb') as f:
        scalers[symbol] = pickle.load(f)


async def bot_main():
    await send_telegram_message("Бот начал анализ рынка...")

    while True:
        tasks = [analyze_symbol(symbol, exchange, current_states, models[symbol],
                                scalers[symbol]) for symbol in symbols]
        await asyncio.gather(*tasks)
