from selenium import webdriver
from time import sleep
from urllib.request import urlretrieve
from datetime import datetime
from PIL import Image
from utils import *
import numpy as np
from keras.preprocessing import image
import cv2
import tensorflow as tf
import unicodedata
from os import path

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

def loadVoteCount():
    if path.exists("vote_count.txt"):
        with open('vote_count.txt','r') as f:
            return int(f.read())
    else:
        with open('vote_count.txt','w') as f:
            f.write('0')
        return 0
    
def saveVoteCount(count):
    with open('vote_count.txt','w') as f:
            f.write(str(count))

def addVoteCount():
    v = loadVoteCount()+1
    saveVoteCount(v)

def vote_with_model(url):
    driver.get(url)
    sleep(delay)
    select_participant(driver,delay,option)
    while True:
        images = crop_image(get_captcha())
        answer = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[1]/span[2]'.format(option)).text
        answer = strip_accents(answer)
        predictions = [get_category(img)[0] for img in images]
        if answer in predictions:
            click_by_index(predictions.index(answer))
            sleep(5)
            try:
                vote_again = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[3]/div/div/div[1]/div[2]/button')
                vote_again.click()
                addVoteCount()
                sleep(1.5)
                select_participant(driver,delay,option)
                continue
            except:
                #Bad prediction
                sleep(delay)
        
        new_image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{}]/div[2]/div/div/div[3]/button'.format(option))
        new_image.click()
        sleep(delay)

def start_bot(opt, mail, password,url='-1',delay_ = 4):
    if url == '-1':
        url = loadCredentials()['URL']

    global delay
    delay = delay_
    global option
    option = opt
    global driver
    driver = get_driver("Chrome")

    global CATEGORIES
    CATEGORIES = get_answers()

    global model
    model = tf.keras.models.load_model("CAPTCHA_model_new.model")
    model.load_weights('CAPTCHA_model_new.h5')
    login(driver,delay,mail,password)
    while True:
        try:
            vote_with_model(url)
        except:
            pass


if __name__ == '__main__':
    cred = loadCredentials()
    start_bot(cred['option'],cred['mail'],cred['password'])
