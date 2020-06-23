from flask import Flask, render_template, request, url_for, redirect 
#from current_mode import current_quality
import datetime
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 


df = pd.read_pickle('1hr_sim.p')

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





#a = get_curr_value(lookup_time, df)



'''defining air quality indicator'''
def current_quality(curr_time, indicator_value):
    """This function classifies air quality into 'healthy', 'moderate', and 'unhealthy'."""
    if indicator_value < 100: 
        return curr_time, "Current air quality is Healthy"
    elif 100 <= indicator_value < 250: 
        return curr_time, "Current air quality is Moderate"
    else: 
        return curr_time, "Current air quality is Unhealthy"

  
#current_quality(a, indicator_value)




app = Flask(__name__)
start_time = datetime.datetime(2020, 6, 10, 10, 5, 0, 234)
#lookup_time = start_time


@app.route('/')
#@app.route('/home')
def home():
    global start_time
    start_time += datetime.timedelta(seconds=300)
    lookup_time = start_time 
    print("current time", lookup_time)
    _, air_qual_val = get_curr_value(lookup_time, df)
    air_qual_val  = round(air_qual_val, 2)
    indicator_value = get_curr_value(lookup_time, df)[-1]  
    air_qual_class = current_quality(lookup_time, indicator_value)[-1]
    return render_template('base.html', 
                            win_size="1", 
                            air_qual_val=str(air_qual_val),
                            air_qual_class=air_qual_class,
                            air_time=str(lookup_time)
                            )



@app.route('/five_min', methods=['GET', 'POST'])
def five_min():
    return render_template('five.html')

@app.route('/main_return', methods=['GET', 'POST'])
def main_return():
    return render_template('base.html') #there is a small problem here, when it returns back to base.html home() does not see to run without clicking the button. It's not consistent but will do for now. 

#app.route('/history')
#def home2():
    #return redirect(url_for('127.0.0.1:5004/five_min'))



@app.route('/ten_min', methods=['GET', 'POST'])
def ten_min():
    return render_template('ten.html')


@app.route('/thirty_min', methods=['GET', 'POST'])
def thirty_min():
    return render_template('base.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5004)
