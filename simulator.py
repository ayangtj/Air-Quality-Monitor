
import datetime
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 


'''
dateTime = datetime.datetime.now()
timestamp = dateTime.isoformat('|')[0:18]

random_reading = []
for i in range(0, 500):
    n = random.uniform(80, 600)
    random_reading.append(round(n,3))
print(timestamp, random_reading) 

# sensor_data = (timestamp, round(n, 3))
'''




'''
for sensor_data in range(500):
    print(sensor_data)
# This part only loops over int
'''




'''
columns = ['Timestamp', 'pm2.5']

sensor_data = {
    'Timestamp': timestamp, 
    'pm2.5': n
}

df = pd.DataFrame(columns=columns)

for x in range(500):
    sensor_data = random.choice(sensor_data.keys())
    
'''




curr_t = datetime.datetime(2020, 6, 10, 10, 0, 0, 0)
print('start simulation at', curr_t)
t_list = []
v_list = []

for i in range(3600):
    tdelta = datetime.timedelta(seconds=random.random() + 0.5)
    curr_t = curr_t + tdelta
    reading = random.random() * 500 # based on realistic pm2.5 values
    print(curr_t, reading)
    t_list.append(curr_t)
    v_list.append(reading)


t_arr = np.array(t_list) #x plot
v_arr = np.array(v_list) # y plot 

columes = ['Timestamp', 'pm2.5']

sensor_data_dict = {
    'Timestamp': t_arr,
    'pm2.5': v_arr
}

df= pd.DataFrame(sensor_data_dict)
df.to_csv('1hr_sim.csv')


