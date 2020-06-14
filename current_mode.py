
import datetime
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 


df = pd.read_csv('1hr_sim.csv')
df

def find_index_of_most_recent(datetime_array, datetime_obj):
    tup = np.where(datetime_array < datetime_obj)
    index_array = tup[0]
    idx = index_array[-1] # last index of index array
    return idx

def get_curr_value(lookup_time, df):
    t_arr = df['Timestamp']
    v_arr = df['pm2.5']
    find_index_of_most_recent_timestamp = find_index_of_most_recent(t_arr, lookup_time)
    idx = find_index_of_most_recent_timestamp
    most_recent_timestamp = t_arr[idx]
    most_recent_value = v_arr[idx]
    print(most_recent_timestamp, most_recent_value)
    return most_recent_timestamp, most_recent_value

t = datetime.datetime(2020, 6, 10, 10, 5, 30, 234)
lookup_time = t.strftime('%y-%m-%d %I:%M:%S.%f')
get_curr_value(lookup_time, df)




def current_quality(most_recent_value):
    if most_recent_value < 25: 
        print("Current air quality is Healthy")
    elif 25 <= most_recent_value < 100: 
        print("Current air quality is Moderate")
    else: 
        print("Current air quality is Unhealthy")
     
current_quality(most_recent_value)
