import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###########  The following code is nearly identical to Day 3 Activity 10 
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
######  There are 2 tables in the db
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
###### Everything you need here can be found in Day 3 Activity 10
@app.route("/")
def welcome():
    """List all available api routes."""
    return ( 
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


###### the 'precipitation' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    Last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    # Query for the date and precipitation for the last year
    last_12_months = dt.date(2017,8,23) - dt.timedelta(days= 365)

    # Dict with date as the key and prcp as the value
    prcp = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= last_12_months, measurement.prcp != None).\
        order_by(measurement.date).all()
    
    prcp_t = []
    for result in prcp:
        row = {}
        row["date"] = prcp[0]
        row["prcp"] = prcp[1]
        prcp_t.append(row)

    return jsonify(prcp_t)

  

###### the 'stations' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    stations_query = session.query(station.name, station.station)

    session.close()
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())
    # Unravel results into a 1D array and convert to a list


###### the 'tobs' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    Last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    # Query the primary station for all tobs from the last year
    last_12_months = dt.date(2017,8,23) - dt.timedelta(days= 365)

    temperature = session.query(measurement.tobs).\
        filter(measurement.date >= last_12_months, measurement.station == 'USC00519281').\
         order_by(measurement.tobs).all()
    # Unravel results into a 1D array and convert to a list
    U_temperature = []
    for date, tobs in temperature:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["tobs"] = tobs
        temperature_totals.append(temperature_dict)

    return jsonify(U_temperature)
    # Return the results


###### the 'temp' route you will query the data with params in the url and return the data Day 3 Activity 10
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
  
    # calculate TMIN, TAVG, TMAX with start and stop
def start_date(start):
    calc_start_temp = stats(start)
    t_temp= list(np.ravel(calc_start_temp))

    TMIN = t_temp[0]
    TAVG = t_temp[1]
    TMAX = t_temp[2]
    TDICT = {'Minimum temperature': TMIN, 'Avg temperature': TAVG, 'Maximum temperature': TMAX, }

    return jsonify(TDICT)


    # Unravel results into a 1D array and convert to a list



if __name__ == '__main__':
    app.run()
