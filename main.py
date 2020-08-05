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

'''imports data simulator to generate data table'''
from package.simulator import *

'''imports funtions for current reading and historic reading'''
from package.functions import * 


'''unpacks simulated data table'''
df = pd.read_pickle('1hr_sim.p')



app = Flask(__name__)
'''Start the simulator at 10:00:06'''
start_time = df.loc[df.index[0], 'Timestamp'] + datetime.timedelta(seconds=500) # got this from file! + 5 secs
current_time = start_time
#print(current_time) = 10:00:06


'''remove static/images folder each time before server starts running, and recreate new image files to ensure the static folder serve the correct image files.'''
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
    '''increase timestamp by 3 seconds each reading, dsipaly current time on the main page

    takes the average reading of the past 5 seconds (-win_size+1, 1) as average air quality value. Send email to user when the average air quality value is above 150

    email subject: Air Quality Alert 
       sender's eamil: aquser41@gmail.com
       receiver's email: aquser41@gmail.com
       sender's email password: python#project1
       email content: on xdate xtime, your air quality became unhealthy. Air quality reading was averaging x.
       
    Display air quality value, air quality class, and air quality message in html file, render html template.'''
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
    avg_air_qual_val = total / win_size   # average value of past 5 seconds 
    avg_air_qual_val_reading = round(avg_air_qual_val, 2)
    
    
    sender_email = 'aquser41@gmail.com' #email security reference has been adjusted  
    receiver_email = 'aquser41@gmail.com'   

    subject = 'Air Quality Alert' #email subject 

    sender_password = 'python#project1' #sender_email password 
        

    yag = yagmail.SMTP(user=sender_email, password=sender_password) #using yagmail SMTP to send emails 

    contents = [
        f"On {current_time}, your air quality became unhealthy. Air quality reading was averaging {avg_air_qual_val_reading}." #email content 
    ]
    if avg_air_qual_val > 150: # When avg_air_qual_val > 150, <triggers email>
        yag.send(to=receiver_email, subject=subject, contents=contents)
    else:
        pass
    
    # get last sec
    lookup_time, air_qual_val = get_curr_value(current_time, df)
    air_qual_class = current_quality(current_time, air_qual_val)
    air_qual_val  = round(air_qual_val, 2) # I'm doing this after the classification
                                           # to reflect the true value for that datetime A combination of a date and a time. Attributes: () 
                                           # the round is just a cosmetic thing
    air_qual_msg = f"Air quality is {air_qual_class}"
    air_time_msg = "Time reported sample was taken: " + lookup_time.strftime("%m/%d/%Y, %H:%M:%S")

    return render_template('base.html', 
                            air_qual_val=str(air_qual_val),
                            air_qual_class=air_qual_msg,
                            air_time=air_time_msg,
                            )


def get_past_X_min(curr_time, min, df):
    ''' return subset of the last min minutes in df, counting backwards from curr_time to x seconds
        return df frame: 
        frame begins from time in past
        frame ends with current time'''
    time_in_past = current_time - datetime.timedelta(minutes=min)
    print("getting data for time from", time_in_past, 'to', curr_time) # DEBUG
    return df[(df['Timestamp'] > time_in_past) & (df['Timestamp'] <= current_time)] 




@app.route('/five_min', methods=['GET', 'POST'])
def five_min():
    '''return past five minutes of air quality and visulize data
    
    Args: 
        1. stops at current time
        2. begins at past 5 min
        3. section of df
        
    saves new section as new (smaller) df 
    plots image and saves to static folder
    
    return: 
        saved image in html '''
    global current_time
    history_5 = get_past_X_min(current_time, 5, df) #past 5 min
    history_5.plot(x='Timestamp', y='pm2.5', marker='.')
    save_images_to = './static/images/' # saves img to relative static folder 
    ts = str(int(current_time.timestamp())) #uses stringyfied current time timestamp as image file name when it's generated 
    fname = save_images_to + ts + ".png"
    plt.savefig(fname)
    #plt.show() for debugging
    return render_template('five.html', img=fname)
      


@app.route('/ten_min', methods=['GET', 'POST'])
def ten_min():
    '''return past ten minutes of air quality and visulize data
    
    Args: 
        1. stops at current time
        2. begins at past 10 min
        3. section of df
        
    saves new section as new (smaller) df 
    plots image and saves to static folder
    
    return: 
        saved image in html '''
    global current_time
    history_10 = get_past_X_min(current_time, 10, df) #past 10 min
    history_10.plot(x='Timestamp', y='pm2.5', marker='.')
    save_images_to = './static/images/'
    ts = str(int(current_time.timestamp())) #uses stringyfied current time timestamp as image file name when it's generated 
    fname = save_images_to + ts + ".png"
    plt.savefig(fname)
    #plt.show() for debugging
    return render_template('ten.html', img=fname)



@app.route('/thirty_min', methods=['GET', 'POST'])
def thirty_min():
    '''return past thirty minutes of air quality and visulize data
    
    Args: 
        1. stops at current time
        2. begins at past 30 min
        3. section of df
        
    saves new section as new (smaller) df 
    plots image and saves to static folder
    
    return: 
        saved image in html '''
    global current_time
    history_30 = get_past_X_min(current_time, 30, df) #past 30 minutes
    history_30.plot(x='Timestamp', y='pm2.5', marker='.')
    save_images_to = './static/images/'
    ts = str(int(current_time.timestamp())) #uses stringyfied current time timestamp as image file name when it's generated 
    fname = save_images_to + ts + ".png"
    plt.savefig(fname)
    #plt.show() for debugging 
    return render_template('thirty.html', img=fname)



@app.route('/main_return', methods=['GET', 'POST'])
def main_return():
    '''Return to Main Page'''
    return render_template('base.html') 


if __name__ == '__main__':
    app.run(debug=True, port=5006)
