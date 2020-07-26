import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
from flask import Flask, render_template, request, url_for, redirect 
import datetime
import time
import random
import numpy as np
import pandas as pd
import yagmail



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
    if indicator_value < 50: 
        return "Healthy"
    elif 50 <= indicator_value < 150: 
        return "Moderate"
    else: 
        return "Unhealthy"


app = Flask(__name__)
#start_time = datetime.datetime(2020, 6, 10, 10, 5, 0, 234) 
start_time = df.loc[df.index[0], 'Timestamp'] + datetime.timedelta(seconds=500) # got this from file! + 5 secs
current_time = start_time
#print(current_time) = 10:00:06


# remove static/images folder and recreate it so we get rid of old images
import shutil, os
try:
    shutil.rmtree("./static/images")
except Exception as e:
    print(e) # no such folder exists, that's fine, ignore error
try:
    os.mkdir("./static/images")
except Exception as e:  
    print(e) # folder already exists, that's OK, ignore


@app.route('/')
def home():
    global current_time

    try:
        add_secs = float(request.args["add_secs"]) # jump ahead X seconds
    except:
        add_secs = 3 # add_secs was not used in URL, just assume real time mode of 3 sec jumps
    
    current_time += datetime.timedelta(seconds=add_secs) # jump x seconds ahead
    print("current time", current_time)

    win_size = 5
    total = 0
    for n in range(-win_size+1, 1): # last win_size secs
        t = datetime.timedelta(seconds=n)
        lookup_time, air_qual_val = get_curr_value(current_time+t, df) # lookup is when the reported sample was actually taken
        total += air_qual_val 
    avg_air_qual_val = total / win_size   # average value
    avg_air_qual_val_reading = round(avg_air_qual_val, 2)
    
    #def send_email(self):
    sender_email = 'aquser41@gmail.com' #email security reference has been adjusted for this project 
    receiver_email = 'aquser41@gmail.com'

    subject = 'Air Quality Alert'

    sender_password = 'python#project1'
        #fill in the password for the email to sent when triggered

    yag = yagmail.SMTP(user=sender_email, password=sender_password)

    contents = [
        f"On {current_time}, your air quality became unhealthy. Air quality reading was averaging {avg_air_qual_val_reading}."
    ]
    if avg_air_qual_val > 150: # When avg_air_qual_val > 250, <triggers email>
        yag.send(to=receiver_email, subject=subject, contents=contents)
    else:
        pass
    
    # get last sec
    lookup_time, air_qual_val = get_curr_value(current_time, df)
    air_qual_class = current_quality(current_time, air_qual_val)
    air_qual_val  = round(air_qual_val, 2) # I'm doing this after the classification
                                           # b/c you want the true value for that datetime A combination of a date and a time. Attributes: () 
                                           # the round is just a cosmetic thing
    air_qual_msg = f"Air quality is {air_qual_class}"
    air_time_msg = "Time reported sample was taken: " + lookup_time.strftime("%m/%d/%Y, %H:%M:%S")

    return render_template('base.html', 
                            air_qual_val=str(air_qual_val),
                            air_qual_class=air_qual_msg,
                            air_time=air_time_msg,
                            )

def get_past_X_min(curr_time, min, df):
    ''' return subset of  the last min minutes in df, counting back from curr_time'''
    time_in_past = current_time - datetime.timedelta(minutes=min)
    print("getting data for time from", time_in_past, 'to', curr_time) # DEBUG
    return df[(df['Timestamp'] > time_in_past) & (df['Timestamp'] <= current_time)]   

@app.route('/five_min', methods=['GET', 'POST'])
def five_min():
    global current_time
    history_5 = get_past_X_min(current_time, 5, df)
    history_5.plot(x='Timestamp', y='pm2.5', marker='.')
    save_images_to = './static/images/' # this is relative to your AIR-QUALITY-MONITOR folder, which contains the server .py file
    ts = str(int(current_time.timestamp()))
    fname = save_images_to + ts + ".png"
    plt.savefig(fname)
    #plt.show()
    return render_template('five.html', img=fname)
      

@app.route('/ten_min', methods=['GET', 'POST'])
def ten_min():
    global current_time
    history_10 = get_past_X_min(current_time, 10, df)
    history_10.plot(x='Timestamp', y='pm2.5', marker='.')
    save_images_to = './static/images/'
    ts = str(int(current_time.timestamp()))
    fname = save_images_to + ts + ".png"
    plt.savefig(fname)
    #plt.show()
    return render_template('ten.html', img=fname)


@app.route('/thirty_min', methods=['GET', 'POST'])
def thirty_min():
    global current_time
    history_30 = get_past_X_min(current_time, 30, df)
    history_30.plot(x='Timestamp', y='pm2.5', marker='.')
    save_images_to = './static/images/'
    ts = str(int(current_time.timestamp()))
    fname = save_images_to + ts + ".png"
    plt.savefig(fname)
    #plt.show()
    return render_template('thirty.html', img=fname)


# This is actually not needed, I just return to / directly
# if you need to send something from one of the history pages back to /
# use a hidden input (see example in five.html) but be aware that 
# / then has to catch that!
@app.route('/main_return', methods=['GET', 'POST'])
def main_return():
    return render_template('base.html') #there is a small problem here, when it returns back to base.html home() does not see to run without clicking the button. It's not consistent but will do for now. 


# remove these 2 lines if you want to run this code on pythonanywhere
if __name__ == '__main__':
    app.run(debug=True, port=5006)
