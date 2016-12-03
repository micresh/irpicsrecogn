from keras.models import Model
from keras.layers import Input, Dense

import numpy as np

outputs = 20
n = 36864

inp = Input(shape=(n,)) # 1d vector as inputdata
hidden_1 = Dense(0.1*n, activation='tanh')(inp)
out = Dense(outputs,activation='sigmoid')(hidden_1)
model = Model(input=inp, output = out)
model.compile(optimizer='rmsprop', 
              loss = 'mean_absolute_error',
              metrics=['mse'])

