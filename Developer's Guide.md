# Developer's Guide

## Overview 

The Air Quality Monitor displays the current air pm2.5 reading and refreshes every three seconds by default. The app also sends emails to user alerting unhealthy air condition when the average pm2.5 reading of the past five seconds exceeds 150. The app is run on flask server. It offers three settings of historic mode, the past five minutes, the past ten minutes, and the past thirty minutes. The app fetches the historical data and plots the image to display. 

## Project Specs 

- Current mode display
- Emails sent to user alerting sub-optimal air quality 
- Historic mode (three settings)

## Install/Deployment/Admin issues: 

## Walkthrough 

- Data structure 




- User starts the app by running the main.py file in terminal. 
  - Code: The generate_simulated_data function (package.simulator.py) runs and generates dataframe with scale=400, offset=30, num_secs=3600, random_state=random_state.
- User checks the current air pm2.5 reading displays on flask web, refreshes every three seconds by default. 
  - Code: The get_index_of_most_recent_timestamp function (package.simulator.py) runs and returns the last index of the index array.  
  - Code: The get_curr_value funtion (package.functions.py) runs (inside def home(): flask function), finds the very last array and returns air quality value, air quality classification, and air quality message. 
  - html template (base.html) is rendered.
- User receives emails alerting that the air quality value is above 150 and the air quality is unhealthy. 
  - Code: The get_curr_value function (package.functions.py) runs once the server is live, and constantly checks the average reading of last five seconds. 
  - Code: The current_quality function (package.functions.py) classifies the average reading of last five seconds to "Healthy", "Moderate", and "Unhealthy". When the classification shows "Unhealthy", an email with date, time, air quality reading, and air quality message is sent to user alerting unhealthy air quality. 
- User clicks on the [Past Five Minute] button, new window loads and displays graphic of past five minutes. User clicks on [Return] button to easily return to the main page.  
  - Code: The get_past_X_min function (main.py) runs and returns the last five minutes section of the df, and saves it as a (smaller) new df. 
  - Code: The new df then gets plotted and saved as a png file and saved in the relative static folder. html template (five.html) is rendered with png file displayed. 
  - Code: The def main_return() funtion (main.py) runs and renders base.html template to return to the main page. 
  - (The same flow applies to the [Past Ten Minutes] and the [Past Thirty Minutes] interactions.) 

## Known Issues 

- No known issue at this point. 

## Future Work

- User Management can be implemented, including creating and managing multiple user account.  
- If not full user management, the user input funciton can be implemented for any user who installs this app to have the option to input their own email address to receive the unhealthy air quality alerts.  

