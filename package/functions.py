import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
from flask import Flask, render_template, request, url_for, redirect 
import datetime
#import time
import random
import numpy as np
import pandas as pd

'''Unpacks simulator data table '''
df = pd.read_pickle('1hr_sim.p')





def get_index_of_most_recent_timestamp(datetime_array, datetime_obj):
    ''' given a datetime object (timestamp), return the (index to) the most recent timestamp within and
    array of  ordered timestamps (datetime_array)
    datetime_array: [12.3, 23.43, 45.4] (using floats for illustration)
    datetime_obj: 25.2
    return: 1 b/c datetime_array[1] i.e. 23.43 is the most recent timestamp
    '''
    tup = np.where(datetime_array < datetime_obj)
    index_array = tup[0]
    idx = index_array[-1] # last index of index array
    return idx


def get_curr_value(current_time, df):
    '''finds the pm2.5 value in dataframe df that was most recently taken before Timestamp.
    returns that most recent timestamp and its pm2.5 value'''
    t_arr = df['Timestamp']
    v_arr = df['pm2.5']
    get_index_of_most_recent_timestamp_timestamp = get_index_of_most_recent_timestamp(t_arr, current_time)
    idx = get_index_of_most_recent_timestamp_timestamp
    most_recent_timestamp = t_arr[idx]
    most_recent_value = v_arr[idx]
    #print(most_recent_timestamp, most_recent_value)
    return most_recent_timestamp, most_recent_value



def current_quality(curr_time, indicator_value):
    '''classifies air quality (indicator_value) at current time (curr_time)
       and returns a string: 'healthy', 'moderate', and 'unhealthy'.
       air quality is healthy if the pm2.5 is lower than 50,
       air qulity is moderate if the pm2.5 is btween 50 and 150,
       air quality is unhealthy if the pm2.5 is over 150.
    ''' 
    if indicator_value < 50: 
        return "Healthy"
    elif 50 <= indicator_value < 150: 
        return "Moderate"
    else: 
        return "Unhealthy"




