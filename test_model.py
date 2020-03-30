import cv2
import tensorflow as tf
import numpy as np
import os
from keras.preprocessing import image
import random
from PIL import Image
from matplotlib import pyplot as plt

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

def remove_stripes(img):
    black = (0,0,0)
    px = img.load()
    brk = False
    for i in range(53):
        for j in range(53):
            if px[i,j] == black and px[i,j+7] == black and px[i,j+14] == black and px[i,j+21] == black and px[i,j+28] == black:
                for k in range(5):
                    for x in range(53):
                        up = px[x,j+7*k-1]
                        down = px[x,j+7*k+1]
                        img.putpixel((x,j+7*k),(round((up[0]+down[0])/2),round((up[1]+down[1])/2),round((up[2]+down[2])/2)))
                brk = True
                break
            if brk:
                break
    return img

def crop_image(file_name):
    left = 0
    top = 0
    bottom = 53
    right = 53
    images = []
    for i in range(5):
        im = Image.open("captcha.png")
        im1 = im.crop((left,top,right,bottom)).convert("RGB")
        im1 = remove_stripes(im1)
        im1.save('temp.png')
        images.append(load_image('temp.png'))
        left += 53
        right += 53
    return images

def plot_image(i, predictions_array, img):
  predictions_array, img = predictions_array[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  color = 'black'

  plt.xlabel("{} {:2.0f}%".format(CATEGORIES[predicted_label],
                                100*np.max(predictions_array)),
                                color=color)

for i in range(1,100):
    print("({}).png:".format(i))
    for image in crop_image("({}).png".format(i)):
        print('\t',get_category(image))
    input()
    

'''
for i in range(1,100):
    images = np.array(crop_image("({}).png".format(i)))
    predictions = model.predict(images)
    # Plota o primeiro X test images, e as labels preditas, e as labels verdadeiras.
    # Colore as predições corretas de azul e as incorretas de vermelho.
    num_rows = 1
    num_cols = 5
    num_images = num_rows*num_cols
    plt.figure(figsize=(2*2*num_cols, 2*num_rows))
    for i in range(num_images):
      plt.subplot(num_rows, 2*num_cols, 2*i+1)
      plot_image(i, predictions, images)
    plt.show()
    
'''
