# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:03:24 2020

@author: Thomas
"""

import random
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

# slave = pd.read_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\MesureVitesseSlave8.txt", header=None, sep=",")
# master =pd.read_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\releve_vitesse_2.txt", header=None, sep=",")

# res = pd.DataFrame()

# res['index'] = slave.iloc[:,0]
# res['interval(ms)'] = slave.iloc[:,2]
# res['time(ms)'] = slave.iloc[:,3]

# res['command_slave'] = slave.iloc[:, 1]
# res['position_slave'] = slave.iloc[:, 4]
# res['speed_slave'] = slave.iloc[:, 5]

# res['command_master'] = master.iloc[:slave.shape[0], 1]
# res['position_master'] = master.iloc[:slave.shape[0], 4]
# res['speed_master'] = master.iloc[:slave.shape[0], 5]

# force = []
# for i in range(slave.shape[0]):
#     force.append( round( random.uniform(0, 10) ,2 ) )
    

# res['force'] = force

# print(res.head())
# print(res.tail())

# export_csv = res.to_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\data_slave_and_master.txt")


DATA_FRAME_COLUMNS = ['index',
                      'interval(ms)',
                      'time(ms)',
                      'command_slave',
                      'position_slave',
                      'speed_slave',
                      'command_master',
                      'position_master',
                      'speed_master',
                      'force']

res = pd.DataFrame(columns=DATA_FRAME_COLUMNS)

index = []
for i in range(57):
    index.append(i)
res['index'] = index

interval_ms = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(9997, 10001) ,0 )
    interval_ms.append( int(random_float) )
res['interval(ms)'] = interval_ms

time_ms = [14083]
for i in range(1, res.shape[0]):
    time_ms.append( time_ms[i-1] + interval_ms[i-1] )
res['time(ms)'] = time_ms

command_slave = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(2170, 2400) ,0 )
    command_slave.append( int(random_float) )
res['command_slave'] = command_slave

position_slave = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(0, -1300) ,0 )
    position_slave.append( int(random_float) )
res['position_slave'] = position_slave

speed_slave = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(-7, 0) ,1 )
    speed_slave.append(random_float)
res['speed_slave'] = speed_slave

command_master = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(2170, 2400) ,0 )
    command_master.append( int(random_float) )
res['command_master'] = command_master

position_master = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(2170, 2200) ,0 )
    position_master.append( int(random_float) )
res['position_master'] = position_master

speed_master = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(-7, 0) ,1 )
    speed_master.append(random_float)
res['speed_master'] = speed_master

force = []
for i in range(res.shape[0]):
    random_float = round( random.uniform(0, 10) ,2 )
    force.append(random_float) 
res['force'] = force

print(res.head(10))
print(res.tail(10))

export_csv = res.to_csv("D:\\Thomas_Data\\GitHub\\didactic_palpation_device\\src\\data_master_and_slave_manually_generated.txt",
                        header=False,
                        index=False,)