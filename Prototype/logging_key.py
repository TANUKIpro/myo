# -*- coding: utf-8 -*-
import threading
import time
from pynput.keyboard import Key, Listener

def key_judge(key):
    if key.char == 'r':
        print("\nROCK")
        R_frag = True
        
    if key.char == 's':
        print("\nSCISSR")
        S_flag = True
        
    if key.char == 'p':
        print("\nPAPER")
        P_flag = True

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

def key_main():
    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()
        
def call_key():
    while True:
        print("a")
        time.sleep(1)

if __name__ == '__main__':
    thread_1 = threading.Thread(target=key_main)
    thread_2 = threading.Thread(target=call_key)

    thread_1.start()
    thread_2.start()
        
