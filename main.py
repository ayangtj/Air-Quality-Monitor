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

from package.functions import * 

from package.simulator import *

df = pd.read_pickle('1hr_sim.p')



app = Flask(__name__)
'''Start the simulator at 10:00:06'''
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
    
    '''Send email to user when past five sencnd's average reading is above 150'''
    sender_email = 'aquser41@gmail.com' #email security reference has been adjusted  
    receiver_email = 'aquser41@gmail.com'

    subject = 'Air Quality Alert'

    sender_password = 'python#project1'
        

    yag = yagmail.SMTP(user=sender_email, password=sender_password)

    contents = [
        f"On {current_time}, your air quality became unhealthy. Air quality reading was averaging {avg_air_qual_val_reading}."
    ]
    if avg_air_qual_val > 150: # When avg_air_qual_val > 150, <triggers email>
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



'''Get past five minutes of air quality and visulize data'''
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
      

'''Get past ten minutes of air quality and visulize data'''
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


'''Get past thirty minutes of air quality and visulize data'''
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


'''Return to Main Page'''
@app.route('/main_return', methods=['GET', 'POST'])
def main_return():
    return render_template('base.html') #there is a small problem here, when it returns back to base.html home() does not see to run without clicking the button. It's not consistent but will do for now. 


# remove these 2 lines if you want to run this code on pythonanywhere
if __name__ == '__main__':
    app.run(debug=True, port=5006)
