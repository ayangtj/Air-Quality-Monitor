
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




df = pd.read_csv('1hr_sim.csv')
df


p = df.plot(x='Timestamp', y='pm2.5', marker='.')
plt.show()
plt.savefig('1hr.png')