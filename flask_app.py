from flask import Flask, render_template, request, url_for, redirect 
#from current_mode import current_quality
import datetime
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 


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


'''defining air quality indicator'''  # CH: not needed as you already have a doc string
# Yes, it's weird to not have anything above the def so if you want you could have
# some sort of header above it - but use normal # for that
def current_quality(curr_time, indicator_value):
    """classifies air quality (indicator_value) at current time (curr_time)
       and returns a string: 'healthy', 'moderate', and 'unhealthy'.
    """

    # CH I don't understand why you return curr_time. Why would
    # the user of the function need something returned that he
    # already gave the function? This would only make sense
    # if your function CHANGES curr_time, then the call would be
    # ct = current_quality(ct, indicator_value)
    # updated              old

    # Also, it's way more flexible to return just the 'core' message 
    # and leave it up to the caller to wrap that core into a nicer message. 
    if indicator_value < 100: 
        return "Healthy"
    elif 100 <= indicator_value < 250: 
        return "Moderate"
    else: 
        return "Unhealthy"


app = Flask(__name__)
start_time = datetime.datetime(2020, 6, 10, 10, 5, 0, 234)
current_time = start_time
win_size = 1 # window size for lookup

@app.route('/')
def home():
    global current_time, win_size
    # current initially is the same as start, every time we trigger /, we add some seconds 
    current_time += datetime.timedelta(seconds=30) # could be random num seconds
    print("current time", current_time)
    lookup_time, air_qual_val = get_curr_value(current_time, df) # lookup is when the reported sample was actually taken
    #indicator_value = get_curr_value(current_time, df)[-1]  # not needed
    air_qual_class = current_quality(current_time, air_qual_val)
    air_qual_val  = round(air_qual_val, 2) # I'm doing this after the classification
                                           # b/c you want the true value for thatdatetime A combination of a date and a time. Attributes: () 
                                           # the round is just a cosmetic thing
    air_qual_msg = f"Air quality is {air_qual_class}"
    air_time_msg = "Time reported sample was taken: " + lookup_time.strftime("%m/%d/%Y, %H:%M:%S")

    return render_template('base.html', 
                            win_size=str(win_size), 
                            air_qual_val=str(air_qual_val),
                            air_qual_class=air_qual_msg,
                            air_time=air_time_msg,
                            )


@app.route('/five_min', methods=['GET', 'POST'])
def five_min():
    return render_template('five.html')

@app.route('/ten_min', methods=['GET', 'POST'])
def ten_min():
    return render_template('ten.html')


@app.route('/thirty_min', methods=['GET', 'POST'])
def thirty_min():
    return render_template('base.html')


# This is actually not needed, I just return to / directly
# if you need to send something from one of the history pages back to /
# use a hidden input (see example in five.html) but be aware that 
# / then has to catch that!
@app.route('/main_return', methods=['GET', 'POST'])
def main_return():
    return render_template('base.html') #there is a small problem here, when it returns back to base.html home() does not see to run without clicking the button. It's not consistent but will do for now. 


# remove these 2 lines if you want to run this code on pythonanywhere
if __name__ == '__main__':
    app.run(debug=True, port=5004)
