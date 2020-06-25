
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random as rd

def generate_simulated_data(scale=90, offset=10, random_state:int=42):
    rnd_state = np.random.RandomState(random_state)
    time = np.arange(0, 2000, 1) # 2000 samples
    pure = 50*np.sin(time/(10*np.pi)) # 1. number affects the amplitude, 2. the wavelength

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
    df['with_jitter'] = df['Value'] + jitter
   
    # As per the 68-95-99.7 rule(also known as the empirical rule) mu+-2*sd 
    # covers 95.4% of the dataset.
    # Since, anomalies are considered to be rare and typically within the 
    # 5-10% of the data; this filtering  technique might work 
    # for us(https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule)
    anomaly_index = np.where(np.abs(df['with_jitter']) > (mu + 2*sd))[0]
    print(f"Number of points further away: {len(anomaly_index)}. Indexes: {anomaly_index}")
    # Generate points uniformly and embed it into the dataset
    for n in range(rd.randint(20, 500)): # anomaly width is between 20 and 500 samples
        random = rnd_state.uniform(0, 2, 1)
        try: # sometimes one of my set of indices overshoots
            df.loc[anomaly_index+n, 'with_jitter'] += random*df.loc[anomaly_index+n, 'with_jitter']
        except:
            pass    
    df['with_jitter'] = abs(df['with_jitter']) # make positive
    df['with_jitter'] /= max(df['with_jitter']) # normalize 0 - 1.0
    df['with_jitter'] *= scale
    df['with_jitter'] += offset

    # make time random and add to df
    time = []
    ct = 0
    for t in range(2000): # must be the same as for num above!
        ct += 1 + rd.random()  # 1 - 2 secs per sample (avg 1.5)
        time.append(ct)
    time = np.array(time)
    df['time'] = time

    return df

# never below 20 never above 80 + 20
# random state is unique, i.e. 100 will always give you the same sampling
df = generate_simulated_data(scale=80, offset=20, random_state=100)
print(df.head())
ax = sns.lineplot(x="time", y="with_jitter", data=df) #,  marker=".")
plt.show()