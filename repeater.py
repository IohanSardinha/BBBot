from pynput import mouse
from pynput import keyboard
from time import sleep, time
from PIL import ImageGrab as screen

class move:
    def __init__(self,x,y,delay):
        self.position = (x,y)
        self.delay = delay

    def play(self):
        sleep(self.delay)
        mouse_controller.position = self.position

class click:
    def __init__(self, button, delay):
        self.button = button
        self.delay = delay

    def play(self):
        sleep(self.delay)
        mouse_controller.click(self.button, 1)

class keypress:
    def __init__(self, key, delay):
        self.key = key
        self.delay = delay

    def play(self):
        sleep(self.delay)
        
        keyboard_controller.press(self.key)

class waitColor:
    def __init__(self):
        self.position = mouse_controller.position
        self.color = screen.grab().getpixel(self.position)
        print(self.color)
        print(self.position)

    def play(self):
        timeout = 0
        print('waiting...')
        color = screen.grab().getpixel(self.position) 
        while (not color == self.color) and (timeout < 120):
            print(color == self.color)
            sleep(1)
            timeout += 1
            color = screen.grab().getpixel(self.position)
        print('done waiting')

def on_move(x, y):
    if not stopped:
        global last_time
        curr_time = time()
        actions.append(move(x,y,curr_time - last_time))
        last_time = curr_time

def on_click(x, y, button, pressed):
    if not pressed and not stopped:
        global last_time
        curr_time = time()
        actions.append(click(button,curr_time - last_time))
        last_time = curr_time
    
def on_press(key):
    print(key)
    global last_time
    if key == keyboard.Key.shift:
        global stopped
        stopped = not stopped
        if not stopped:
            global last_time
            last_time = time()
            print('Unpaused')
        else:
            print('Paused')

    if key == keyboard.Key.ctrl_l:
        print('will wait for color')
        actions.append(waitColor())

    elif not stopped and not key == keyboard.Key.esc:
        curr_time = time()
        actions.append(keypress(key,curr_time - last_time))
        last_time = curr_time

def on_release(key):
    if key == keyboard.Key.esc:
        mouse_listener.stop()
        keyboard_listener.stop()
        for i in range(10):
            playActions()
        return False

def playActions():
    print('Playing...')
    for action in actions:
        action.play()
    print('Finished!')

mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click)

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()
stopped = False
last_time = time()
actions = []
mouse_listener.start()
keyboard_listener.start()
print('Observing moovement')
