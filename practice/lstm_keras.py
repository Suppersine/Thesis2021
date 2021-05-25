import pandas
import matplotlib.pyplot as plt
import theano
import tensorflow
from tensorflow import keras

dataset = pandas.read_csv('airline-passengers.csv', usecols=[1], engine='python', encoding="utf-8")
plt.plot(dataset)
plt.show()

