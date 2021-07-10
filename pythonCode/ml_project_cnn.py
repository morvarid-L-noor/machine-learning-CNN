# -*- coding: utf-8 -*-
"""ML-project-CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QVoFZjf6MQ6kxj8zR9nKA5fIwqi8aKou
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout,MaxPooling2D,Conv2D ,Activation
from keras.optimizers import SGD
#from tensorflow import set_random_seed
import matplotlib.pyplot as plt
from keras.datasets import fashion_mnist
from keras.utils import np_utils
from keras import backend as K
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def show(image, label):
  plt.figure()
  plt.imshow(image)
  plt.axis('off')
  plt.title(class_names[label])
  plt.show()

# loading dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

"""* CNN :

**hiden layers activation function : relu  , optimizer : adam , with dropout**
"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)


model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

batch_size = 32
epochs = 8

history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 1))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model.save("model_{}.hd5".format(pos))

Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**hiden layers activation function : relu  , optimizer : adam , without dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.20))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
#model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)


model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

epochs = 8

batch_size = 32

history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 1))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model.save("model_{}.hd5".format(pos))

model = keras.models.load_model('/content/model_1.hd5')
Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**hiden layers activation function : relu  , optimizer : SGD , with dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
sgd = keras.optimizers.SGD(learning_rate=0.001)

model.compile(loss='sparse_categorical_crossentropy',
              optimizer= sgd,
              metrics=['accuracy'])

model.summary()

batch_size = 32
epochs = 8
#model.fit(X, y, callbacks=[saver], epochs=5)

history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 1))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
model.save("model_{}.hd5".format(pos))
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model = keras.models.load_model('/content/model_1.hd5')
Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**hiden layers activation function : relu  , optimizer : SGD , without dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.20))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
#model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
sgd = keras.optimizers.SGD(learning_rate=0.001)

model.compile(loss='sparse_categorical_crossentropy',
              optimizer= sgd,
              metrics=['accuracy'])

model.summary()

epochs = 8

batch_size = 32
#model.fit(X, y, callbacks=[saver], epochs=5)

history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 1))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
model.save("model_{}.hd5".format(pos))
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model = keras.models.load_model('/content/model_7.hd5')
Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**hiden layers activation function : sigmoid  , optimizer : adam , with dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='sigmoid',input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2), activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))

model.add(Flatten())
model.add(Dense(128, activation='sigmoid'))
model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)


model.compile(loss='sparse_categorical_crossentropy',
              optimizer= 'adam',
              metrics=['accuracy'])

model.summary()

batch_size = 32
epochs = 8
history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 1))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
model.save("model_{}.hd5".format(pos))
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model = keras.models.load_model('/content/model_1.hd5')
Y_pred = model.predict(x_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test,axis = 1) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(Y_true, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**hiden layers activation function : sigmoid  , optimizer : adam , without dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
input_layer=layers.Input(shape=np.shape(data[0]))
p0=layers.MaxPooling2D(pool_size=(2,2))
hidden_layer_1=layers.Conv2D(20,kernel_size=(5,5),activation='sigmoid')
p1=layers.MaxPool2D(pool_size=(2,2))
hidden_layer_2=layers.Conv2D(40,kernel_size=(3,3),activation='sigmoid')
hidden_layer_3=layers.Flatten()
hidden_layer_4=layers.Dense(450,activation='sigmoid')
output_layer=layers.Dense(10,activation='softmax')
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='sigmoid', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(20, kernel_size=(5,5),activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.20))
model.add(Conv2D(40, kernel_size=(3, 3),activation='sigmoid'))
model.add(Flatten())
model.add(Dense(450, activation='sigmoid'))
#model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)


model.compile(loss='sparse_categorical_crossentropy',
              optimizer= 'adam',
              metrics=['accuracy'])

model.summary()

batch_size = 32
epochs = 8
history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 1))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
model.save("model_{}.hd5".format(pos))
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

#from sklearn.metrics import plot_confusion_matrix
Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

'''plot_confusion_matrix(model, X_test, y_test)  
plt.show() '''

Y_true.shape

"""**hiden layers activation function : sigmoid  , optimizer : SGD , with dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='sigmoid', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2),activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))

model.add(Flatten())
model.add(Dense(128, activation='sigmoid'))
model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
sgd = keras.optimizers.SGD(learning_rate=0.001)


model.compile(loss='sparse_categorical_crossentropy',
              optimizer= sgd,
              metrics=['accuracy'])

model.summary()

batch_size = 32
epochs = 16
history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 3))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
model.save("model_{}.hd5".format(pos))
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model = keras.models.load_model('/content/model_15.hd5')
Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**hiden layers activation function : sigmoid  , optimizer : SGD , without dropout**"""

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28, 28, 1)
X_test = X_test.reshape(X_test.shape[0],28, 28, 1)

'''from tensorflow import set_random_seed

set_random_seed(432)
np.random.seed(234)
'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='sigmoid', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(2, 2), activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.20))
model.add(Flatten())
model.add(Dense(128, activation='sigmoid'))
#model.add(Dropout(0.4))
model.add(Dense(10, activation='softmax'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
sgd = keras.optimizers.SGD(learning_rate=0.001)


model.compile(loss='sparse_categorical_crossentropy',
              optimizer= sgd,
              metrics=['accuracy'])

model.summary()

batch_size = 32
epochs = 8
history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=0.25)

plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['font.size'] = 16
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Validation loss')
x_ticks = np.arange(0, epochs + 1, 5)
x_ticks [0] += 1
plt.xticks(x_ticks)
plt.ylim((0, 3))
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.title("Epochs-Loss for CNN")
plt.legend()
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pos = np.argmin(history.history['val_loss'])
model.save("model_{}.hd5".format(pos))
print("The epoch with the minimum validation loss is:", pos)
print("The Train Accuracy is: {0:.5f}".format(history.history['accuracy'][pos]))
print("The Validation Accuracy is: {0:.5f}".format(history.history['val_accuracy'][pos]))


loss, accuracy = model.evaluate(X_test, y_test)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

model = keras.models.load_model('/content/model_7.hd5')
Y_pred = model.predict(X_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(y_test, Y_pred_classes) 
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, 
            classes = ['T-shirt/Top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot'])

"""**with normalizing : ..............................................**"""

X_train = X_train /255.0 
X_test = X_test /255.0

"""----------------------------------------------------------------------------"""

# normalizing dataset from 0 to 1
train_images, test_images = train_images/255., test_images/255.

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle-boot']

index = 256
show(train_images[index], train_labels[index])

# sequential class 
model = keras.Sequential([
                          keras.layers.Flatten(input_shape=(28, 28)),
                          keras.layers.Dense(10, activation='softmax')
])

# declaring optimizer for network
model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(), metrics='accuracy')

# trainig process by 5 epochs
model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))

# model evaluation
index = 10
print(model.predict(test_images[index:index+1]))
print(np.sum(model.predict(test_images[index:index+1])))
predicted = np.argmax(model.predict(test_images[index:index+1]))
print(class_names[predicted])
show(test_images[index], predicted)

