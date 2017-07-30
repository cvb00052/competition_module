# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:08:34 2017

@author: RXYH

for complete nerual network

"""


from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, normalization, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from keras import regularizers
import get_picture
import os, re


path_pic = 'C:/Users/RXYH/Desktop/train/train_twenty_thousand'
path_label = 'C:/Users/RXYH/Desktop/train/data_train_lable_twenty_thousand.txt'
#path_pic_test = 'C:/Users/RXYH/Desktop/train/test1_for_train'
path_pic_test = 'C:/Users/RXYH/Desktop/train/image'
#path_label_test = 'C:/Users/RXYH/Desktop/train/val.txt'

#(x_test, y_test) = get_picture.load_data(path_label_test, path_pic_test)
x_test = get_picture.load_data_test(path_pic_test)
(x_train, y_train) = get_picture.load_data(path_label, path_pic)

#x_train = x_train.reshape(8154, 128, 128, 3)
y_train = np_utils.to_categorical(y_train, num_classes = 134)
#y_test = np_utils.to_categorical(y_test, num_classes = 134)
 
model = Sequential()

model.add(Convolution2D(
    input_shape = (70, 70, 3),
    filters = 64,
    kernel_size = 5,
    strides = (1, 1),
    padding = 'valid',
    data_format = 'channels_last',
))

model.add(Activation('relu'))
model.add(normalization.BatchNormalization())
model.add(MaxPooling2D(
    pool_size = 2,
    strides = 2,
    padding = 'same',
    data_format = 'channels_last',
))


model.add(Convolution2D(
    32, 5, strides=(1, 1), padding='same', data_format= 'channels_last'
))
model.add(Activation('relu'))
model.add(normalization.BatchNormalization())
model.add(MaxPooling2D(
    pool_size=2, strides=2, padding='same', data_format='channels_last'
))

model.add(Flatten())
model.add(Dense(512, kernel_regularizer = regularizers.l2(0.01)))
model.add(Activation('relu'))



model.add(Dense(512, kernel_regularizer = regularizers.l2(0.01)))
model.add(Activation('relu'))



model.add(Dense(134))
model.add(Activation('softmax'))

#adam = Adam(lr = 3e-4)
adam = Adam(lr = 2e-4)

model.compile(
    optimizer = adam,
    loss = 'categorical_crossentropy',
    metrics = ['accuracy']
)

print('Training-------------')
model.fit(x_train, y_train, epochs = 10 , batch_size=40 , verbose = 1)

#print('Testing--------------')
#loss, accurr = model.evaluate(x_test, y_test, batch_size = 40, verbose = 1)
#
#print(loss, accurr)



print('Testing--------------')
arr = model.predict(x_test, batch_size=40, verbose=1)

kpath = 'C:/Users/RXYH/Desktop/train/image'
with open('C:/Users/RXYH/Desktop/train/result.txt', mode = 'w') as f:
    imgs = os.listdir(kpath)
    rule_picname = r'\b(\d*,+\d*).'
    compile_pic = re.compile(rule_picname);
    for i in range(len(imgs)):
        num = 0
        maxpro = 0
        newpath = kpath + '/' + imgs[i]
        if newpath == kpath + '/Thumbs.db':
            continue
        for k in range(134):
            if maxpro < arr[i][k]:
                num = k
                maxpro = arr[i][k]
        strname = compile_pic.findall(imgs[i])
        data_name = strname[0]
        seq = [str(num) + '\t' + str(data_name) + '\n']
        f.writelines(seq)

