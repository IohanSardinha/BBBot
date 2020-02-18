from tkinter import *
from PIL import ImageTk, Image
from functools import partial
from utils import get_answers
from pathlib import Path
from utils import get_answers

def button_action(btn):
    global img
    global curr_img
    global curr_img_text
    im = Image.open('objects/ ({0}).png'.format(curr_img))
    im.save('train/'+btn+('/({0}).png'.format(curr_img)))
    curr_img += 1
    img = ImageTk.PhotoImage(Image.open('objects/ ({0}).png'.format(curr_img)))
    panel = Label(m,image = img)
    panel.place(x=400-30,y=20)
    curr_img_text.set('({}).png'.format(curr_img))

if __name__ == '__main__':

    for fold in get_answers():
        Path("train/"+fold+"/").mkdir(parents=True, exist_ok=True)

    m = Tk()
    m.geometry("800x500")

    try:
        f = open("last",'r')
        r = [line for line in f]
        curr_img = int(r[0])
        f.close()
    except:
        curr_img = 1
        
    img = ImageTk.PhotoImage(Image.open('objects/ ({0}).png'.format(curr_img)))
    panel = Label(m,image = img)
    panel.place(x=400-26,y=20)
    curr_img_text = StringVar()
    curr_img_label = Label(m,textvariable=curr_img_text)
    curr_img_text.set('({}).png'.format(curr_img))
    curr_img_label.place(x= 400-25,y=80)

    words = sorted(get_answers())

    pos = 0
    cols = 6
    rows = 10
    for i in range(cols):
        for j in range(rows):
            t = words[pos]
            action = partial(button_action,t)
            button = Button(m,text=t,width = 16,command= action)
            button.place(x=20+i*130,y=150+j*30)
            pos+= 1
            
    m.mainloop()
    f = open("last",'w')
    f.write(str(curr_img))
    f.close()
