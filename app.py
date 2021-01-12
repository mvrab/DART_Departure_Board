from flask import Flask, render_template

import requests
import re
from bs4 import BeautifulSoup
import datetime

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


app = Flask('Spring Valley Station Departures')

@app.route('/')
def index():
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

    entrytemplate ='        <div class="w3-round-xlarge w3-safety-{{ n1c }}">\n          <div class="w3-row">\n            <div class="w3-col w3-dark-grey w3-right w3-text-white w3-center w3-round-xlarge compact" style="width:100px">\n              <h1><b>{{ n1t }}</b></h1>\n              <h4>Minutes</h4>\n            </div>\n            <div class="w3-rest w3-margin-left">\n              <h2>{{ n1d }}</h2>\n            </div>\n          </div>\n        </div>\n        <div class="w3-margin-bottom"></div>\n'
    
    
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

    return render_template('index.html', southtext=southtext, northtext=northtext)

if __name__ == '__main__':
    app.run()
