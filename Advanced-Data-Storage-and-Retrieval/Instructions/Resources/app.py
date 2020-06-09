#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 16:42:13 2020

@author: pariya
"""

# 1. import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify

import datetime as dt
from datetime import timedelta
from datetime import date

#%% 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#%% #. Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

#%%
@app.route("/")
def home():
    print("Pariya, Server received request for 'Home' page...")
    return "Welcome to Climate App!"

#%%
@app.route("/api/v1.0/pricipitation")
def precip():
    
    q1 = """ 
            SELECT date, prcp
            FROM measurement
            WHERE date 
            BETWEEN '2016-08-23' 
            AND '2017-08-23';  
        """
    
    results = pd.read_sql(q1, engine)
    
    results_json = results.to_json(orient='records')
    
    return results_json
    
    #Create a list of dictionary with 'date' as keys and 'prcp' as values
    #precip_list = []
    
    #for result in results:
        
     #   precip_dict = {}
     #   precip_dict["date"] = results[0]
     #   precip_dict["prcp"] = results[1]
     #   precip_list.append(precip_dict)

     # return jsonify(precip_list)

#%%
@app.route("/api/v1.0/station")
def station():
    
    results = pd.read_sql('SELECT station, name FROM station', engine)

    results_json = results.to_json(orient='records')

    return results_json

#%%
@app.route("/api/v1.0/tobs")
def tobs():
    
    q2 = """
            SELECT  station as most_active_station,
                    date, 
                    tobs as temp, 
                    COUNT(*) AS count_frequency
            FROM measurement
            WHERE date BETWEEN '2016-08-23' AND '2017-08-23'
            GROUP BY station
            ORDER BY count_frequency DESC LIMIT 1;
        """
    
    results = pd.read_sql(q2, engine)
    
    results_json = results.to_json(orient='records')

    return results_json
     
#%%
@app.route("/api/v1.0/<start>")
def search1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    post_date = dt.timedelta(days=365)
    start = start_date - post_date
    end =  dt.date(2017, 8, 23)
    
    q3 = """ 
            SELECT  date,
                    MIN(tobs) as min_temp,
                    MAX(tobs) as max_temp,
                    AVG(tobs) as avg_temp
            FROM measurement
            WHERE date >= start_on
            AND date < end_on;
        """
    results = pd.read_sql(q3, engine)
    
    results_json = results.to_json(orient='records')

    return results_json

#%%
@app.route("/api/v1.0/<start>/<end>")
def search2(start, end):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end,'%Y-%m-%d')
    post_date = dt.timedelta(days=365)
    start = start_date - post_date
    end =  end_date - last_year
    
    q4 = """ 
            SELECT  date,
                    MIN(tobs) as min_temp,
                    MAX(tobs) as max_temp,
                    AVG(tobs) as avg_temp
            FROM measurement
            WHERE date >= start_on
            AND date < end_on;
        """
    results = pd.read_sql(q4, engine)
    
    results_json = results.to_json(orient='records')

    return results_json



#%%
if __name__ == "__main__":
    app.run(debug=True)