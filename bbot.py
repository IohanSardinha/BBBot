from tkinter import *
import vote_bot
from functools import partial
import threading
from credentials import VOTE_URL
from credentials import mail as MAIL
from credentials import password as PASSWORD
from credentials import VOTE_OPTION


def start(mail,password,option,delay,url):
    #print(mail.get(),password.get(),url.get())
    process = threading.Thread(target=vote_bot.start_bot,args=(int(option.get()),mail.get(),password.get(),url.get(),int(delay.get()),))
    process.start()

if __name__ == '__main__':
    m = Tk()
    m.geometry("230x300")
    m.title("BBBot")
    m.iconphoto(False, PhotoImage(file='logo.png'))
    m.resizable(False,False)

    usernameLabel = Label(m,text="Usuário")
    usernameLabel.place(x=20,y=10)

    usernameEntry = Entry(m,width=30)
    usernameEntry.insert(0,MAIL)
    usernameEntry.place(x=20,y=30)

    passwordLabel = Label(m,text="Senha")
    passwordLabel.place(x=20,y=50)

    passwordEntry = Entry(m,width=30,show="*")
    passwordEntry.insert(0,PASSWORD)
    passwordEntry.place(x=20,y=70)

    urlLabel = Label(m,text="URL votação")
    urlLabel.place(x=20,y=90)

    urlEntry = Entry(m,width=30)
    urlEntry.insert(0,VOTE_URL)
    urlEntry.place(x=20,y=110)

    delayLabel = Label(m,text="Tempo entre cliques. Ajuste de acordo")
    delayLabel.place(x=10,y=130)
    delayLabel2 = Label(m,text="com a velocidade da internet")
    delayLabel2.place(x=10,y=150)

    delayEntry = Scale(m,from_=1, to=5,resolution=0.1,orient=HORIZONTAL)
    delayEntry.set(2.5)
    delayEntry.place(x=55,y=170)

    optionLabel = Label(m,text="Eliminado (1 a 3 de cima para baixo)")
    optionLabel.place(x=20,y=210)

    optionEntry = Entry(m,width=30)
    optionEntry.insert(0,VOTE_OPTION)
    optionEntry.place(x=20,y=230)

    action = partial(start,usernameEntry,passwordEntry,optionEntry,delayEntry,urlEntry)
    startButton = Button(m,text="Começar", command=action)
    startButton.place(x=80,y=260)

    m.mainloop()
