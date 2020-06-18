from flask import Flask, render_template, request, url_for, redirect 
#from current_mode import current_quality
import datetime
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 

app = Flask(__name__)


df = pd.read_pickle('1hr_sim.p')
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
    #print(most_recent_timestamp, most_recent_value)
    return most_recent_timestamp, most_recent_value

lookup_time = datetime.datetime(2020, 6, 10, 10, 5, 30, 234)
#lookup_time = t.strftime('%y-%m-%d %I:%M:%S.%f')
get_curr_value(lookup_time, df)

a = get_curr_value(lookup_time, df)
a


#defining air quality indicator
def current_quality(a, indicator_value):
    if indicator_value < 100: 
        print(a, "Current air quality is Healthy")
    elif 100 <= indicator_value < 250: 
        print(a, "Current air quality is Moderate")
    else: 
        print(a, "Current air quality is Unhealthy")

indicator_value = get_curr_value(lookup_time, df)[-1]    
current_quality(a, indicator_value)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')





@app.route('/result/', methods=['GET'])
def result():
    print(request.args['a'])
    print(request.args['indicator_value'])

 




if __name__ == '__main__':
    app.run(debug=True)
