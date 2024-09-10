# Import the dependencies.
import numpy as np
import flask 
print(flask.__version__)
import sqlalchemy
print(sqlalchemy.__version__)
import datetime as dt
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# home page with all available routes to view api data
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )

# setting up the route for the 'percipitation' api
@app.route("/api/v1.0/percipitation")
def percipitation():
    session = Session(engine)
    # Starting from the most recent data point in the database. 
    most_recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results_rain = session.query(measurements.date, measurements.prcp).filter(measurements.date >= one_year_ago).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    measurements_df = pd.DataFrame(results_rain, columns=['Date', 'Precp'])

    # Set the 'Date' column as the index
    measurements_df.set_index('Date', inplace=True)

    # Sort the dataframe by date
    measurements_df = measurements_df.sort_index()
    
    # closing session
    session.close()

    # converting to normal list for JSON
    rain_fall = list(np.ravel(results_rain))

    # creating JSON
    return jsonify(rain_fall)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    # List the stations and their counts in descending order.
    station_counts = session.query(measurements.station, func.count(measurements.station).label('count'))\
                            .group_by(measurements.station)\
                            .order_by(func.count(measurements.station).desc())\
                            .all()

    stations_count = list(np.ravel(station_counts))
    return jsonify(stations_count)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Starting from the most recent data point in the database. 
    most_recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query the last 12 months of temperature data for the most active station
    most_active_station = session.query(measurements.station)\
                                  .group_by(measurements.station)\
                                  .order_by(func.count(measurements.station).desc())\
                                  .first()[0]

    temps = session.query(measurements.date, measurements.tobs)\
                   .filter(measurements.station == most_active_station)\
                   .filter(measurements.date >= one_year_ago)\
                   .all()

    # Convert the results to a list
    temps = list(np.ravel(temps))

    session.close()  
    return jsonify(temps)  

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    # query for the min, avg, and max temps
    results = session.query(func.min(measurements.tobs),
                            func.avg(measurements.tobs),
                            func.max(measurements.tobs)
                         )\
                        .filter(measurements.date >= start)\
                        .all()
    
    session.close()

    # create a dictionary to hold the results
    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    # Query for the minimum, average, and maximum temperatures from the start date to the end date
    results = session.query(func.min(measurements.tobs), 
                            func.avg(measurements.tobs), 
                            func.max(measurements.tobs))\
                     .filter(measurements.date >= start)\
                     .filter(measurements.date <= end)\
                     .all()

    session.close()

    # Create a dictionary to hold the results
    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temp_data)
    