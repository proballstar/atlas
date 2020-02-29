import skyforce
import tensorflow as tf

# @NOTE This will be taken and given to the server.py,or it will be import via the file importation with functions
#Add the functions to be able to use measure and collect data 
def load_data(url):
    return url

def create_model():
    model = tf.keras.Sequential([
        tf.keras.Dense(1)
    ])