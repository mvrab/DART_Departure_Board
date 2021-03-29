from flask import Flask, render_template

import requests
import re
from bs4 import BeautifulSoup
import datetime
#import webbrowser
import os
#from threading import Timer

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

def get_parameters(selectedtrain):
    ################
    ###   TIME   ###
    ################

    timepattern = r"((1[0-2]|0?[1-9])\:([0-5]?[0-9])\s?(?:AM|PM|am|pm))"
    currentTime = datetime.datetime.now()

    x = re.findall(timepattern, selectedtrain[5])
    arrivalTimeM = datetime.datetime.strptime(x[0][0], '%I:%M %p')
    arrivalTime = arrivalTimeM.replace(day=currentTime.day, month=currentTime.month, year=currentTime.year)
    n1t = str(round((arrivalTime - currentTime).total_seconds()/60%1440)-1)
    if (int(n1t) > 1000) or (int(n1t) < 0): n1t = "Now"


    #######################
    ###   DESTINATION   ###
    #######################

    n1d = str(selectedtrain[3])[3:-4].title()
    if (n1d == 'Dfw'):
        n1d = 'DFW Airport'


    #################
    ###   COLOR   ###
    #################

    colorpattern = r'<b>(.+?) LINE'

    n1c_string = str(selectedtrain[1])
    n1c = re.findall(colorpattern, n1c_string)[0].lower()

    return (n1d, n1t, n1c)


app = Flask('Spring Valley Train Times', template_folder='/home/pi/dart/templates')
global refresh_counter
refresh_counter = 0

@app.route('/')
def index():
    global refresh_counter
    try:
        response = requests.get('https://m.dart.org/railSchedule.asp?switch=pushRailStops3&ddlRailStopsFrom=26672&option=1')
        soup = BeautifulSoup(response.text, 'html.parser')
        allTrains = soup.findAll('div', id=lambda x: x and x.startswith('table'))
    
        northboundtrains = []
        southboundtrains = []
    
        for train in allTrains:
            if ((str(list(train)[3])[3:-4].title()) == 'Parker Road'):
                northboundtrains.append(train)
            else:
                southboundtrains.append(train)
        # getText() return the text between opening and closing tag
    
        entrytemplate ='        <div class="w3-round-xlarge w3-safety-{{ n1c }}">\n          <div class="w3-row w3-display-container">\n            <div class="w3-col w3-dark-grey w3-right w3-text-white w3-center w3-round-xlarge compact" style="width:100px">\n              <h5 class="w3-margin-top"><b>{{ n1t }}</b></h5>\n              <h4>Minutes</h4>\n            </div>\n            <div class="w3-rest w3-margin-left w3-display-left">\n              <h1>{{ n1d }}</h1>\n            </div>\n          </div>\n        </div>\n        <div class="w3-margin-bottom"></div>\n'
    
    
        northentry = ''
        for train in northboundtrains:
            temporaryentrytemplate = entrytemplate
            parameter_list = list(train)
            (n1d, n1t, n1c) = get_parameters(parameter_list)
            #print(n1d, n1t, n1c)
    
            temporaryentrytemplate=temporaryentrytemplate.replace("{{ n1d }}", n1d)
            temporaryentrytemplate=temporaryentrytemplate.replace("{{ n1c }}", n1c)
            temporaryentrytemplate=temporaryentrytemplate.replace("{{ n1t }}", n1t)
            northentry += temporaryentrytemplate
    
        southentry = ''
        for train in southboundtrains:
            temporaryentrytemplate = entrytemplate
            parameter_list = list(train)
            (n1d, n1t, n1c) = get_parameters(parameter_list)
            #print(n1d, n1t, n1c)
    
            temporaryentrytemplate=temporaryentrytemplate.replace("{{ n1d }}", n1d)
            temporaryentrytemplate=temporaryentrytemplate.replace("{{ n1c }}", n1c)
            temporaryentrytemplate=temporaryentrytemplate.replace("{{ n1t }}", n1t)
            southentry += temporaryentrytemplate
    
        northtext = northentry.split('\n')
        southtext = southentry.split('\n')
        
        clock_time_obj = datetime.datetime.now()
        clockstr = clock_time_obj.strftime("%I:%M %p")
        if clockstr[0] == "0":
            clockstr = clockstr[1:]
        refresh_counter = 0
        
        return render_template('index.html', clockstr=clockstr, southtext=southtext, northtext=northtext)
    except Exception as error:
        #print(error)
        refresh_counter += 1
        if refresh_counter>5:
            os.system('sudo reboot')
        clock_time_obj = datetime.datetime.now()
        clockstr = clock_time_obj.strftime("%I:%M %p")
        if clockstr[0] == "0":
            clockstr = clockstr[1:]
        return render_template('reload.html', clockstr=clockstr, attemptstr=str(refresh_counter))

#def open_browser():
        #sleep(30)
        #cmd = "chromium-browser --kiosk --force-device-scale-factor=1.00 http://127.0.0.1:5000"
        #os.system(cmd)

if __name__ == '__main__':
        #Timer(1, open_browser).start();
        app.run(port=5000)
