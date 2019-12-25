#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kbhit import *

atexit.register(set_normal_term)
set_curses_term()

try:
    while True:
        if kbhit():
            key = getch()
        
            if   key == 'r': print("ROCK")
            elif key == 's': print("SCISSOR")
            elif key == 'p': print("PAPET")
        else: pass
except(KeyboardInterrupt, SystemExit): print("EXIT")
