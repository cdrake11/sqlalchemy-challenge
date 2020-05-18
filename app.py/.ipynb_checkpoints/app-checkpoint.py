import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()
station = Base.classes.station
measurement = Base.classes.measurement
session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>" 
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
    


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of your dictionary"""
    #last 12 months
    last_year = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year_exact = dt.date(2017,8,23) - dt.timedelta(days=365)
    prec_route= session.query(measurement.date, func.avg(measurement.prcp)).filter(measurement.date>=last_year_exact).group_by(measurement.date).all()
    return jsonify(prec_route)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    stations_route = session.query(station.name, station.station).all()
    return jsonify(stations_route)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year_exact = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp_route = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= last_year_exact, measurement.station == 'USC00519281').order_by(measurement.date.desc()).all()
    return jsonify(temp_route)

@app.route("/api/v1.0/<start>")
def start():
    

@app.route("/api/v1.0/<start>/<end>")
def end():
    

    
if __name__=="__main__":
    app.run()