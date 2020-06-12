
#Back end for historic mode:
#Hard code a good start time
#Plot 5 min, 10 min and 30 min windows 
#Save each plot as a png  (5min.png, 10min.png and 30min.png)


from matplotlib import pyplot
import pandas as pd 



import datetime
import time
import random
import numpy as np




#historical data in the past 30 minutes
curr_t = datetime.datetime(2020, 6, 10, 10, 0, 0, 0)
print('start simulation at', curr_t)
t_list = []
v_list = []

for i in range(18):
    tdelta = datetime.timedelta(seconds=random.random() + 100)
    curr_t = curr_t + tdelta
    reading = random.random() * 150 # based on realistic pm2.5 values
    print(curr_t, reading)
    t_list.append(curr_t)
    v_list.append(reading)


t_arr = np.array(t_list)
v_arr = np.array(v_list)

def find_index_of_most_recent(datetime_array, datetime_obj):
    tup = np.where(datetime_array < datetime_obj)
    index_array = tup[0]
    idx = index_array[-1] # last index of index array
    return idx



