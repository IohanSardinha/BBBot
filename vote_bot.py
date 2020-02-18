from selenium import webdriver
from time import sleep
from urllib.request import urlretrieve
from credentials import mail,password
from datetime import datetime
from PIL import Image
from utils import *
import numpy as np
from keras.preprocessing import image
import cv2
import tensorflow as tf
import unicodedata

def vote_with_human():
    captcha = int(input("Captcha answer: "))-1

    image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[2]/img'.format(option))
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(image, 53*captcha + 10, 5)
    action.click()
    action.perform()

def click_by_index(index):
    image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[2]/img'.format(option))
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(image, 53*index + 26, 26)
    action.click()
    action.perform()

def vote_first():
    captcha = 0

    image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[2]/img'.format(option))
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(image, 53*captcha + 10, 5)
    action.click()
    action.perform()

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

def crop_image(file_name):
    left = 0
    top = 0
    bottom = 53
    right = 53
    images = []
    for i in range(5):
        im = Image.open(file_name)
        im1 = im.crop((left,top,right,bottom)).convert("RGB")
        im1 = remove_stripes(im1)
        im1.save('temp.png')
        images.append(load_image('temp.png'))
        left += 53
        right += 53
    return np.array(images)

def get_captcha():
    image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[2]/img'.format(option))
    src = image.get_attribute('src')
    urlretrieve(src, "captcha.png")
    return 'captcha.png'

def vote_with_model():
    total, wright = 0,1
    driver.get(VOTE_URL)
    sleep(delay)
    select_participant(driver,delay,option)
    while True:
        images = crop_image(get_captcha())
        total += 1
        answer = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[1]/span[2]'.format(option)).text
        answer = strip_accents(answer)
        predictions = [get_category(img)[0] for img in images]
        print(wright/total)
        if answer in predictions:
            click_by_index(predictions.index(answer))
            sleep(delay)
            try:
                vote_again = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[3]/div/div/div[1]/div[2]/button')
                vote_again.click()
                sleep(1.5)
                select_participant(driver,delay,option)
                wright += 1
                continue
            except:
                sleep(delay)
        
        new_image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{}]/div[2]/div/div/div[3]/button'.format(option))
        new_image.click()
        sleep(delay)

if __name__ == '__main__':
   
   VOTE_URL = 'https://gshow.globo.com/realities/bbb/bbb20/votacao/paredao-bbb20-quem-voce-quer-eliminar-babu-lucas-ou-victor-hugo-24ddad72-6fcd-43ff-a9d0-a3e2c4cfa8e3.ghtml'
   delay = 2.5

   option = 2 #Participant to vote, from top to bottom starting with 1

   driver = get_driver("Opera")
    
   CATEGORIES = get_answers()

   model = tf.keras.models.load_model("CAPTCHA.model")
   model.load_weights('CAPTCHA.h5')
   login(driver,delay)
   while True:
      try:
         vote_with_model()
      except:
         pass