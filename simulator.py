
import datetime
import random
import numpy
import pandas as pd 


dateTime = datetime.datetime.now()
timestamp = dateTime.isoformat('|')[0:18]

random_reading = []
for i in range(0, 500):
    n = random.uniform(80, 600)
    random_reading.append(round(n,3))
print(timestamp, random_reading) 

# sensor_data = (timestamp, round(n, 3))





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




