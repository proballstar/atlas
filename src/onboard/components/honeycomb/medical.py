import tensorflow as tf #@TODO(aaronhma): Get the Tenserflow to activate

# @NOTE This will be taken and given to the server.py,or it will be import via the file importation with functions
#Add the functions to be able to use measure and collect data 
def load_data(url):
    # @TODO(aaronhma)" load data"
    return url

def create_model():
    model = tf.keras.Sequential([
        tf.keras.Dense(1), # input layer
    ])
    
def __init__():
    load_data()
    create_model()

def post():
    pass