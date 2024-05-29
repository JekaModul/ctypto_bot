from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.models import load_model as keras_load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


def create_model(look_back):
    model = Sequential()
    model.add(LSTM(50, input_shape=(1, look_back)))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def train_model(data, look_back=1, epochs=20, batch_size=1):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(data)

    trainX, trainY = create_dataset(data, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))

    model = create_model(look_back)
    model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size)

    return model, scaler


def predict_price(model, scaler, last_sequence):
    last_sequence = scaler.transform(last_sequence)
    # Измените форму last_sequence на (1, len(last_sequence))
    last_sequence = np.reshape(last_sequence, (1, len(last_sequence)))
    prediction = model.predict(last_sequence)
    predicted_price = scaler.inverse_transform(prediction)
    return predicted_price[0, 0]


def save_model(model, model_path):
    model.save(model_path)

def load_model(model_path):
    return keras_load_model(model_path)


