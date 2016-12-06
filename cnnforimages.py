from keras.models import Model
from keras.layers import Input, Dense
from tifffile import *
import numpy as np
import csv

window_height = 576
window_width = 200
image_step = window_width
outputs = 10


def test_network(in_data, out_data):
    inp = Input(shape=(window_height, window_width,))  # 3d vector as inputdata
    hidden_1 = Dense(0.1*n, activation='tanh')(inp)
    out = Dense(outputs, activation='sigmoid')(hidden_1)
    model = Model(input=inp, output=out)
    model.compile(optimizer='rmsprop',
                  loss='mse',
                  metrics=['accuracy'])
    model.train_on_batch(in_data, out_data)
    return model.evaluate()


with open('objects.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    objects_coor = []
    for row in reader:
        t = [int(row[0]), int(row[1]), int(row[2])]
        objects_coor.append(t)

for picnum in range(1, 801):
    s = "/home/micresh/traindata/Train1/" + str(picnum) + '.tif'
    tiff = imread(s)
    images_count = 16000/image_step
    objects_on_pic = []
    for i in range(len(objects_coor)):
        if objects_coor[i][0] == picnum:
            objects_on_pic.append([objects_on_pic[i][1], objects_on_pic[i][2]])
    out_data = np.zeros((images_count, 8))
    in_data = np.zeros(((images_count, window_height, window_width)))
    for step in range(images_count):
        for y_cor in range(window_height):
            for x in range(window_width):
                in_data[step][y_cor][x_cor] = tiff[c][n][y_cor][x_cor + image_step * step]
        if len(objects_coor) == 0:
            for x in range(8):
                out_data[step][x] = 0
        else:
            x = 0
            while x < 8:
                for y in range(len(objects_coor)):
                    out_data[step][x] = objects_coor[y][0]
                    out_data[step][x+1] = objects_coor[y][1]
                    x += 2
    print (test_network(in_data, out_data))
