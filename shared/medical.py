from . import skyforce
import tensorflow as tf
import os
import urllib
import pandas as pd
from keras.callbacks import EarlyStopping

rows_to_show = 10

def fetch_data():
    pass

def load_data(atlas_folder):
    data_path = os.path.join(atlas_folder, "")
    return pd.read_csv(data_path)

def create_model():
    model = tf.keras.Sequential([
        tf.keras.Dense(1), # input layer
        tf.keras.Dense(10, activation='relu'), # hidden layer
        tf.keras.Dense(2) # output layer
    ])
    return model

def compile_model(model, eta):
    mae = tf.keras.losses.MeanAbsoluteError()
    sgd = tf.keras.optimizers.SGD(learning_rate=eta, name='SGD')
    model.compile(optimizer=sgd, loss=mae)
    return model
    
def __init__():
    data = load_data()
    X = data[:20] # @TODO: get real data
    y = data[20:] # @TODO: get real data
    print("First 10 rows of data:\n".format(data.head(rows_to_show)))
    create_model()
    compile_model(create_model(), 0.01)
    early_stopping_monitor = EarlyStopping(patience=5)
    create_model().model.fit(X, y, epochs=1000, validation_split=0.3, callbacks=[early_stopping_monitor])
    # @TODO: Wait for post() method to be called

def post():
    print("Post method called!")