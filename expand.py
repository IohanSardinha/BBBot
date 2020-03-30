import cv2
import tensorflow as tf
import numpy as np
import os
from keras.preprocessing import image
import random
from PIL import Image
from matplotlib import pyplot as plt
import shutil

def get_answers():
    f = open("answers.txt",'r')
    r = [line[0:-1] for line in f]
    f.close()
    return r

CATEGORIES = get_answers()

model = tf.keras.models.load_model("CAPTCHA_model_new.model")
model.load_weights('CAPTCHA_model_new.h5')

IMG_SIZE = 53

def load_image(filename):
    img_array = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img_array = np.expand_dims(img_array,axis=0)
    #img_array = img_array.reshape(1,IMG_SIZE,IMG_SIZE,1)
    return img_array

def get_category(image):
    prediction = model.predict(image)
    certanty = np.max(prediction)
    category = CATEGORIES[np.argmax(prediction)]
    return category,certanty

for i in range(1964,6765):
    try:
        image = load_image("objects2\("+str(i)+").png")
        prediction = get_category(image)[0]
        image = Image.open("objects2\("+str(i)+").png")
        image.save("model_classify\{}\ ({}).png".format(prediction,i))
    except:
        pass
