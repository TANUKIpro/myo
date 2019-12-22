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
        self.tytle_dic = {"DATA"   : [["EMG0", "EMG1", "EMG2", "EMG3",
                                     "EMG4", "EMG5", "EMG6", "EMG7", "TIME"]],
                          "STATUS": [["ROCK", "SCISSOR", "PAPER"]]
                          }
        self.plt_graph = True
        self.black_myo = False
        self.white_myo = True
        
        self.tytle_flag    = True
        self.writeEMG_flag = True
        
        self._time = 0
        self.count = 0
        
    def data_plot(self, data):
        x0 = data[:,0]
        x1 = data[:,1]
        x2 = data[:,2]
        x3 = data[:,3]
        x4 = data[:,4]
        x5 = data[:,5]
        x6 = data[:,6]
        x7 = data[:,7]
        t  = data[:,8]
                    
        #Black Myo
        if self.black_myo:
            plt.plot(t, x0, label="EMG D", color='black')
            plt.plot(t, x1, label="EMG E", color='red')
            plt.plot(t, x2, label="EMG F", color='green')
            plt.plot(t, x3, label="EMG G", color='blue')
            plt.plot(t, x4, label="EMG H", color='sienna')
            plt.plot(t, x5, label="EMG A", color='greenyellow')
            plt.plot(t, x6, label="EMG B", color='lightsalmon')
            plt.plot(t, x7, label="EMG C", color='lightpink')
        
        #White Myo
        if self.white_myo:
            plt.plot(t, x0, label="EMG F", color='black')
            plt.plot(t, x1, label="EMG G", color='red')
            plt.plot(t, x2, label="EMG H", color='green')
            plt.plot(t, x3, label="EMG A", color='blue')
            plt.plot(t, x4, label="EMG B", color='sienna')
            plt.plot(t, x5, label="EMG C", color='greenyellow')
            plt.plot(t, x6, label="EMG D", color='lightsalmon')
            plt.plot(t, x7, label="EMG E", color='lightpink')
            
        plt.xlabel("Time[sec]", fontsize=16)
        plt.ylabel("EMG", fontsize=16)
        
        plt.grid()
        plt.legend(loc=1, fontsize=16)
        plt.show()
        
    def save_data(self, saving_path, data):
        if self.tytle_flag is True:
            with open(saving_path, 'w') as f_handle:
                np.savetxt(f_handle, self.tytle_dic["DATA"], delimiter=",", fmt="%s")
            self.tytle_flag = False
            
        with open(saving_path, 'a') as f_handle:
            np.savetxt(f_handle, data, delimiter=",", fmt="%.5f")
    
    def proc_emg(self, emg, moving, times=[]):
        times.append(time.time())
        if len(times) > 20:
            #print((len(times) - 1) / (times[-1] - times[0]))
            times.pop(0)

    def main(self, saving_path):
        m = MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
        m.add_emg_handler(self.proc_emg)
        m.connect()
        
        m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        m.add_pose_handler(lambda p: print('pose', p))
        data2 = np.array([["EMG0", "EMG1", "EMG2", "EMG3",
                         "EMG4", "EMG5", "EMG6", "EMG7", "TIME"]])
        dim_data = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        try:
            t_start = time.time()
            while True:
                m.run(1)
                #stop vibration ever
                m.write_attr(0x19, b'\x03\x01\x00')
                
                emg, self._time = m.plot_emg(t_start)
                
                #グラフは1次元
                dim_data = np.append(emg, self._time)
                print(dim_data)
                if len(dim_data) == 9:
                    dim2_data = np.expand_dims(dim_data, axis=0)
                    data = np.append(data, dim2_data, axis=0)
                    self.count += 1
                
        except KeyboardInterrupt:
            self.save_data(saving_path, data)
        finally:
            m.disconnect()
            print()
            if self.plt_graph:
                self.data_plot(data)

if __name__=='__main__':
    output = OutputUnit()
    output.main('data/temp/sample_EMGdata.csv')
    
