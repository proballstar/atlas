import skyforce
import tensorflow as tf
#Add the functions to be able to use measure and collect data 
def load_data(url):
    return url

def create_model():
    model = tf.keras.Sequential([
        tf.keras.Dense(1)
    ])