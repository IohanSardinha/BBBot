import unicodedata
from selenium import webdriver
from time import sleep
from credentials import mail,password
from PIL import Image

def get_answers():
    try:
        f = open("answers.txt",'r')
        r = [line[0:-1] for line in f]
        f.close()
        return r
    except:
        return []

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def login(driver,delay,eml=mail,passw=password):

    driver.get("https://login.globo.com/login/151")

    email = driver.find_element_by_xpath('//*[@id="login"]')
    email.send_keys(eml)

    pswd = driver.find_element_by_xpath('//*[@id="password"]')
    pswd.send_keys(passw)

    enter = driver.find_element_by_xpath('//*[@id="login-form"]/div[6]/button')
    enter.click()

    sleep(delay)

def select_participant(driver,delay,option):
    participant = driver.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[4]/div[{0}]/div'.format(option))
    participant.click()
    sleep(delay)

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

def get_driver(browser):
    if browser == "Opera":   
       return webdriver.Opera()
    elif browser == "Chrome":
       return webdriver.Chrome()
    elif browser == "Edge":
        return webdriver.Edge()
    else:
       return webdriver.Ie()
