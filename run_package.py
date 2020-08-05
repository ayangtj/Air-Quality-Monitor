import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
from flask import Flask, render_template, request, url_for, redirect 
import datetime
import time
import random
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import random as rd
import os

'''imports data simulator to generate data table'''
from package.simulator import *

'''imports funtions for current reading and historic reading'''
from package.functions import * 



'''
simulates data generation in the format of a wave
https://stackoverflow.com/questions/14058340/adding-noise-to-a-signal-in-python
'''



def generate_simulated_data(scale=90, offset=10, num_secs= 2000, random_state=42):
    '''Generates simlated data with amplitude and wavelength. 

    time loop generates 2000 samples. 

    concatenates on the second axis, which allows mixing different data distribution. 

    jitter: adding gaussian distribution of 0.3 to pm2.5 reading.

    mu+-2*sd: covers 95.4% of the dataset according to the empirical rule.

    for loop: Generate points uniformly and embed it into the dataset, anomaly width is between 20 and 500 samples

    df['pm2.5'] is made positive and and normalized 0-1.0.

    current time starts at 6/10/20, 10:00:00, and increases per second.'''

    # never below 20 never above 80 + 20
    # random state is unique, i.e. 100 will always give you the same sampling
    rnd_state = np.random.RandomState(random_state)
    time = np.arange(0, num_secs, 1) # 2000 samples
    pure = 200*np.sin(time/(30*np.pi)) #amplitude and wavelength 

    # concatenate on the second axis; this will allow us to mix different data 
    # distribution
    data = np.c_[pure]
    mu = np.mean(data)
    sd = np.std(data)
    print(f"Data shape : {data.shape}. mu: {mu} with sd: {sd}")
    df = pd.DataFrame(data, columns=['Value'])
    df['Index'] = df.index.values

    
    jitter = 0.3*rnd_state.normal(mu, sd, size=df.shape[0])
    df['pm2.5'] = df['Value'] + jitter
   
    # As per the 68-95-99.7 rule(also known as the empirical rule) mu+-2*sd 
    # covers 95.4% of the dataset.
    # Since, anomalies are considered to be rare and typically within the 
    # 5-10% of the data; this filtering  technique might work 
    # for us(https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule)
    anomaly_index = np.where(np.abs(df['pm2.5']) > (mu + 2*sd))[0]
    print(f"Number of points further away: {len(anomaly_index)}. Indexes: {anomaly_index}")
    
    for n in range(rd.randint(20, 500)): 
        random = rnd_state.uniform(0, 2, 1)
        try: # sometimes one of my set of indices overshoots
            df.loc[anomaly_index+n, 'pm2.5'] += random*df.loc[anomaly_index+n, 'pm2.5']
        except:
            pass    
    df['pm2.5'] = abs(df['pm2.5']) # make positive
    df['pm2.5'] /= max(df['pm2.5']) # normalize 0 - 1.0
    df['pm2.5'] *= scale
    df['pm2.5'] += offset


    curr_t = datetime.datetime(2020, 6, 10, 10, 0, 0, 0)
    tstamps = []
    for t in time:
        tdelta = datetime.timedelta(seconds=1)
        curr_t = curr_t + tdelta
        tstamps.append(curr_t)

    df['Timestamp'] = tstamps
    return df


'''Packs data into dataframe table where x=Timestamp and y=pm2.5.

    Saves data table into pickle file to perserve the original data type.'''
# never below 20 never above 80 + 20
# random state is unique, i.e. 100 will always give you the same sampling
random_state = 45
df = generate_simulated_data(scale=400, offset=30, num_secs=3600, random_state=random_state)
print(df.head())
ax = sns.lineplot(x="Timestamp", y="pm2.5", data=df) #,  marker=".")
df.to_pickle('1hr_sim.p')
# This is only for debugging purpose.
#save_images_to = '/Users/April/Library/Mobile Documents/com~apple~CloudDocs/HCI 584/Air-Quality-Monitor/static/images'
#plt.savefig(save_images_to + 'new.png')
#plt.show() 
 


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