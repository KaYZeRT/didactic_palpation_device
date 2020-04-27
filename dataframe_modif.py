# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:03:24 2020

@author: Thomas
"""

import random
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

slave = pd.read_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\MesureVitesseSlave8.txt", header=None, sep=",")
master =pd.read_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\releve_vitesse_2.txt", header=None, sep=",")

res = pd.DataFrame()

res['index'] = slave.iloc[:,0]
res['interval(ms)'] = slave.iloc[:,2]
res['time(ms)'] = slave.iloc[:,3]

res['command_slave'] = slave.iloc[:, 1]
res['position_slave'] = slave.iloc[:, 4]
res['speed_slave'] = slave.iloc[:, 5]

res['command_master'] = master.iloc[:slave.shape[0], 1]
res['position_master'] = master.iloc[:slave.shape[0], 4]
res['speed_master'] = master.iloc[:slave.shape[0], 5]

force = []
for i in range(slave.shape[0]):
    force.append( round( random.uniform(0, 10) ,2 ) )
    

res['force'] = force

print(res.head())
print(res.tail())

export_csv = res.to_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\data_slave_and_master.txt")