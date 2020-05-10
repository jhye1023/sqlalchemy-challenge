import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome(): 
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date.between('2016-08-24', '2017-08-23')).all()
    session.close()

    precipitation= []
    for result in results:
        row = {"date":"prcp"}
        row["date"] = result[0]
        row["prcp"] = result[1]
        precipitation.append(row)

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query(Measurement.station).all()
    session.close()

    stations = []
    for station in results:
        if station not in stations:
            stations.append(station)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
                   filter(Measurement.station == "USC00519281").\
                   filter(Measurement.date.between('2016-01-01', '2016-12-31')).all()
    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")

def date_start(start):
    print(start)
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= (start)).all()
    session.close()

    data = list(np.ravel(results))
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    print(start)
    print(end)
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= (start), Measurement.date <= (end)).all()
    session.close()
    
    data_se = list(np.ravel(results))
    return jsonify(data_se)
    

if __name__ == '__main__':
    app.run(debug=True) 
