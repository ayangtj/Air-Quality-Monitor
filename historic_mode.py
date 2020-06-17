
#Back end for historic mode:
#Hard code a good start time
#Plot 5 min, 10 min and 30 min windows 
#Save each plot as a png  (5min.png, 10min.png and 30min.png)


from matplotlib import pyplot as plt 
import pandas as pd 



import datetime
import time
import random
import numpy as np




df = pd.read_pickle('1hr_sim.p')
df
type(df)

p = df.plot(x='Timestamp', y='pm2.5', marker='.')
plt.show()
plt.savefig('1hr.png')





#updated_time = t10_time.strftime('%y-%m-%d %I:%M:%S.%f')

def get_past_10_min(t10_time):
    past_10_min = df.loc[df['Timestamp'] < t10_time]
    return past_10_min

t10_time = datetime.datetime(2020, 6, 10, 10, 10, 0, 0)
df_10 = get_past_10_min(t10_time)
df_10

type(df_10)



'''
df_10 = get_past_10_min(t10_time, df)
'''
p10 = df_10.plot(x='Timestamp', y='pm2.5', marker='.')
plt.show() 
plt.savefig('10min.png')


# past 30 min
def get_past_30_min(t30_time):
    past_30_min = df.loc[df['Timestamp'] < t30_time]
    return past_30_min

t30_time = datetime.datetime(2020, 6, 10, 10, 30, 0, 0)
df_30 = get_past_30_min(t10_time)
df_30



p30 = df_30.plot(x='Timestamp', y='pm2.5', marker='.')
plt.show() 
plt.savefig('30min.png')


# past 50 min
def get_past_5_min(t5_time):
    past_5_min = df.loc[df['Timestamp'] < t5_time]
    return past_5_min

t5_time = datetime.datetime(2020, 6, 10, 10, 5, 0, 0)
df_5 = get_past_5_min(t5_time)
df_5



p5 = df_5.plot(x='Timestamp', y='pm2.5', marker='.')
plt.show() 
plt.savefig('5min.png')