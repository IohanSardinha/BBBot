import numpy as np
import os
from matplotlib import pyplot as plt
import cv2
import random
import numpy as np
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import keras
from keras.preprocessing.image import ImageDataGenerator 
import tensorflow as tf
from utils import get_answers

def create_training_data():
	for category in CATEGORIES :
		path = os.path.join(DATADIR, category)
		class_num = CATEGORIES.index(category)
		for img in os.listdir(path):
			try :
			    img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
			    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
			    training_data.append([new_array, class_num])
			except Exception as e:
			    pass

def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

if __name__ == "__main__":

    file_list = []
    class_list = []

    DATADIR = "train"

    CATEGORIES = get_answers()

    IMG_SIZE = 53

    for category in CATEGORIES :
            path = os.path.join(DATADIR, category)
            for img in os.listdir(path):
                    img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)

    training_data = []

    create_training_data()

    random.shuffle(training_data)

    X = []
    y = []

    for features, label in training_data:
            X.append(features)
            y.append(label)

    train_images = np.array(X)/250.0
    train_labels = np.array(y)
    class_names = CATEGORIES


    model = keras.Sequential()

    model.add(Flatten(input_shape=(IMG_SIZE, IMG_SIZE)))
    model.add(Dense(1024, activation='relu'))

    model.add(Dense(512))
    model.add(Activation("relu"))


    model.add(Dense(256))
    model.add(Activation("relu"))


    model.add(Dense(128))
    model.add(Activation("relu"))

    model.add(Dense(600))
    model.add(Activation("softmax"))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy','mse','mae','mape'])


    model.fit(train_images, train_labels, epochs=1, batch_size = 32, validation_split=0.1)

    test_loss, test_acc, test_mse, mae, mape = model.evaluate(train_images,  train_labels, verbose=2)

    print('\nTest accuracy:', test_acc, '\nTest mse:',test_mse,'\n mae',mae,'\nmape',mape)
    predictions = model.predict(train_images)

    model_json = model.to_json()
    with open("CAPTCHA_model.json", "w") as json_file :
            json_file.write(model_json)

    model.save_weights("CAPTCHA_model.h5")
    print("Saved model to disk")

    model.save('CAPTCHA_model.model')

    num_rows = 5
    num_cols = 3
    num_images = num_rows*num_cols
    plt.figure(figsize=(2*2*num_cols, 2*num_rows))
    for i in range(num_images):
      plt.subplot(num_rows, 2*num_cols, 2*i+1)
      plot_image(i, predictions, train_labels, train_images)
    plt.show()
