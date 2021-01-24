from selenium import webdriver
from time import sleep
from urllib.request import urlretrieve
from datetime import datetime
from PIL import Image
from utils import *
import os
from pathlib import Path

def crop_image(file_name):
    left = 0
    top = 0
    bottom = 53
    right = 53
    num_files = len(os.listdir('objects/'))+1
    for i in range(5):
        im = Image.open(file_name)
        im1 = im.crop((left,top,right,bottom)).convert("RGB")
        im1 = remove_stripes(im1)
        im1.save('objects/'+' b({}).png'.format(num_files))
        print('objects/'+' ({}).png'.format(num_files))
        left += 53
        right += 53
        num_files += 1

def save_answers(o):
    f = open("answers.txt",'w')
    for l in o:
        f.write(l+'\n')
    f.close()

def get_images(size):
    select_participant(driver,delay,option)
    objects = get_answers()
    for i in range(size):
        
        answer = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[1]/span[2]'.format(option)).text
        answer = strip_accents(answer)
        if not answer in objects:
            objects.append(answer)
        
        image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div[2]/div/div/div[2]/div/div[2]/img'.format(option))
        src = image.get_attribute('src')
        now = datetime.now()
        file_name = "img"+now.strftime("%d%m%Y%H%M%S")+".png"
        urlretrieve(src, "original_images/"+file_name)
        crop_image('original_images/'+file_name)
        
        new_image = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{}]/div[2]/div/div/div[3]/button'.format(option) )
        new_image.click()
        sleep(1.8)
        if(i%25 == 0):
            save_answers(objects)
    save_answers(objects)

if __name__ == '__main__':

    Path("original_images/").mkdir(parents=True, exist_ok=True)
    Path("objects/").mkdir(parents=True, exist_ok=True)

    delay = 1

    data_size = 1000
    
    option = 1

    driver = get_driver("Chrome")

    CATEGORIES = get_answers()

    login(driver,delay)
    driver.get(loadCredentials()['URL'])
    get_images(data_size)
    driver.quit()
