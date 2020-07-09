
# modified from https://stackoverflow.com/questions/14058340/adding-noise-to-a-signal-in-python

import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random as rd
import datetime
import os

def generate_simulated_data(scale=90, offset=10, num_secs= 2000, random_state=42):
    rnd_state = np.random.RandomState(random_state)
    time = np.arange(0, num_secs, 1) # 2000 samples
    pure = 200*np.sin(time/(30*np.pi)) # 1. number affects the amplitude, 2. the wavelength

    # concatenate on the second axis; this will allow us to mix different data 
    # distribution
    data = np.c_[pure]
    mu = np.mean(data)
    sd = np.std(data)
    print(f"Data shape : {data.shape}. mu: {mu} with sd: {sd}")
    df = pd.DataFrame(data, columns=['Value'])
    df['Index'] = df.index.values

    # Adding gaussian jitter (0.2 to 0.35 is good
    jitter = 0.3*rnd_state.normal(mu, sd, size=df.shape[0])
    df['pm2.5'] = df['Value'] + jitter
   
    # As per the 68-95-99.7 rule(also known as the empirical rule) mu+-2*sd 
    # covers 95.4% of the dataset.
    # Since, anomalies are considered to be rare and typically within the 
    # 5-10% of the data; this filtering  technique might work 
    # for us(https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule)
    anomaly_index = np.where(np.abs(df['pm2.5']) > (mu + 2*sd))[0]
    print(f"Number of points further away: {len(anomaly_index)}. Indexes: {anomaly_index}")
    # Generate points uniformly and embed it into the dataset
    for n in range(rd.randint(20, 500)): # anomaly width is between 20 and 500 samples
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

# never below 20 never above 80 + 20
# random state is unique, i.e. 100 will always give you the same sampling
random_state = 45
df = generate_simulated_data(scale=400, offset=30, num_secs=3600, random_state=random_state)
print(df.head())
ax = sns.lineplot(x="Timestamp", y="pm2.5", data=df) #,  marker=".")
df.to_pickle('1hr_sim.p')
save_images_to = '/Users/April/Library/Mobile Documents/com~apple~CloudDocs/HCI 584/Air-Quality-Monitor/static/images'
plt.savefig(save_images_to + 'new.png')
plt.show()