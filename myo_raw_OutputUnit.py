#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import time
import numpy as np
import threading
from multiprocessing import Value, Array, Process
from pynput.keyboard import Key, Listener
from matplotlib import pyplot as plt
from myo_raw import MyoRaw
key_list = [0, 0, 0]
class Key_logger:
    def key_judge(self, key):
        key_list = [0, 0, 0]
        if key.char == 'r':
            key_list[0] = 1
            print("\nROCK")
        elif key.char == 's':
            key_list[1] = 1
            print("\nSCISSOR")
        elif key.char == 'p':
            key_list[2] = 1
            print("\nPAPER")
        print(key_list)
        
    def on_press(self, key):
        try:
            self.key_judge(key)
        except AttributeError:
            pass

    def on_release(self, key):
        if key == Key.ctrl:
            print("INFO : <class> Key_logger is ended")
            return False

    def key_main(self):
        with Listener(on_press = self.on_press, on_release = self.on_release) as listener:
            listener.join()
            #print(listener)

class OutputUnit:
    def __init__(self, saving_path):
        self.saving_path = saving_path
        self.tytle_dic = {"DATA"   : [["EMG0", "EMG1", "EMG2", "EMG3",
                                       "EMG4", "EMG5", "EMG6", "EMG7", "TIME", "STATUS"]],
                          "STATUS" : [["ROCK", "SCISSOR", "PAPER"]]
                          }
        self.plt_graph = True
        self.save_csv  = True
        self.byn_np    = True
        
        self.black_myo = False
        self.white_myo = True
        
        self.tytle_flag    = True
        self.writeEMG_flag = True
        
        self._time = 0
        self.count = 0
        
    def data_plot(self, data):
        data = data[1:]
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
        data = data[1:]
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

    def myo_main(self, status):
        m = MyoRaw(None)
        m.add_emg_handler(self.proc_emg)
        m.connect()

        m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
        m.add_pose_handler(lambda p: print('pose', p))
        
        # [EMG0, EMG1, EMG2, EMG3, EMG4, EMG5, EMG6, EMG7, TIME, STATUS]
        dim_data = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
        data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=float)
        try:
            t_start = time.time()
            while True:
                print(status)
                m.run(1)
                #stop vibration ever
                m.write_attr(0x19, b'\x03\x01\x00')
                emg, self._time = m.plot_emg(t_start)
                #グラフは1次元
                dim_data[:9] = np.append(emg, self._time)
                if self._time > 1.:
                    #print(dim_data)
                    if len(dim_data) == 10:
                        dim2_data = np.expand_dims(dim_data, axis=0)
                        data = np.append(data, dim2_data, axis=0)
                self.count += 1
                
        except KeyboardInterrupt:
            pass
        finally:
            m.disconnect()
            if self.save_csv: self.save_data(self.saving_path + ".csv", data[1:])
            if self.byn_np: np.save(self.saving_path, data[1:])
            if self.plt_graph: self.data_plot(data)
            print()

if __name__=='__main__':
    saving_path = 'data/temp/sample_EMGdata'
    output = OutputUnit(saving_path)
    key    = Key_logger()
    
    process_key = Process(target=key.key_main)
    print("INFO : THREAD_1 START")
    process_key.start()
    
    process_myo = Process(target=output.myo_main(key_list))
    print("INFO : THREAD_2 START")
    process_myo.start()
    
    process_key.join()
    process_myo.join()
    
    
