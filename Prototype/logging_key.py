# -*- coding: utf-8 -*-
from pynput.keyboard import Key, Listener

def key_judge(key):
    if key.char == 'r': print("ROCK")
    if key.char == 's': print("SCISSR")
    if key.char == 'p': print("PAPER")

def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        key_judge(key)
    except AttributeError:
        pass

def on_release(key):
    #print('{0} released'.format(key))

    if key == Key.ctrl:
        # Stop listener
        return False

if __name__ == '__main__':
    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()
