#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import enum
import re
import struct
import sys
import threading
import time
import numpy as np
from matplotlib import pyplot as plt

from myo_raw import MyoRaw

class OutputUnit:
    def __init__(self):
        self.EMGandT = []
        
        self.black_myo = False
        self.White_myo = True
    
    def data_plot(self, data):
        data_np = np.array(data)
        x0 = data_np[:,0]
        x1 = data_np[:,1]
        x2 = data_np[:,2]
        x3 = data_np[:,3]
        x4 = data_np[:,4]
        x5 = data_np[:,5]
        x6 = data_np[:,6]
        x7 = data_np[:,7]
        t  = data_np[:,8]
        
        #Black Myo
        if black_myo:
            plt.plot(t, x0, "r-", label="EMG D", color='black')
            plt.plot(t, x1, "r-", label="EMG E", color='red')
            plt.plot(t, x2, "r-", label="EMG F", color='green')
            plt.plot(t, x3, "r-", label="EMG G", color='blue')
            plt.plot(t, x4, "r-", label="EMG H", color='sienna')
            plt.plot(t, x5, "r-", label="EMG A", color='greenyellow')
            plt.plot(t, x6, "r-", label="EMG B", color='lightsalmon')
            plt.plot(t, x7, "r-", label="EMG C", color='lightpink')
        
        #White Myo
        if white_myo:
            plt.plot(t, x0, "r-", label="EMG F", color='black')
            plt.plot(t, x1, "r-", label="EMG G", color='red')
            plt.plot(t, x2, "r-", label="EMG H", color='green')
            plt.plot(t, x3, "r-", label="EMG A", color='blue')
            plt.plot(t, x4, "r-", label="EMG B", color='sienna')
            plt.plot(t, x5, "r-", label="EMG C", color='greenyellow')
            plt.plot(t, x6, "r-", label="EMG D", color='lightsalmon')
            plt.plot(t, x7, "r-", label="EMG E", color='lightpink')
            
        
        plt.xlabel("Time[sec]", fontsize=16)
        plt.ylabel("EMG", fontsize=16)
        
        plt.grid()
        plt.legend(loc=1, fontsize=16)
        plt.show()
    
    def proc_emg(self, emg, moving, times=[]):
        times.append(time.time())
        if len(times) > 20:
            #print((len(times) - 1) / (times[-1] - times[0]))
            times.pop(0)

    def main(self):
        m = MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
        m.add_emg_handler(self.proc_emg)
        m.connect()
        
        m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        m.add_pose_handler(lambda p: print('pose', p))
    
        
        try:
            t_start = time.time()
            while True:
                m.run(1)
                #stop vibration ever
                m.write_attr(0x19, b'\x03\x01\x00')
                emg, t = m.plot_emg(t_start)
                try:
                    self.EMGandT.append([emg[0],emg[1],emg[2],emg[3],emg[4],emg[5],emg[6],emg[7], t])
                except:
                    pass
        except KeyboardInterrupt:
            pass
        finally:
            m.disconnect()
            print()
            data_plot(self.EMGandT)

if __name__=='__main__':
    output = OutputUnit()
    output.main()
