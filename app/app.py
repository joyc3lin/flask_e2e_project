from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, text

load_dotenv()  

AZUREURL = os.getenv("AZURE")

engine = create_engine(AZUREURL,
    connect_args={'ssl': {'ssl-mode':'preferred'}},
)    


app = Flask(__name__)   

@app.route('/')
def mainpage():
    return render_template('base.html')

@app.route('/patients')
def patients():
    # Establish a database connection
    with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
        query1 = text('SELECT * FROM patients')

        result1 = connection.execute(query1)

        # Fetch all rows of data
        patientdata = result1.fetchall()

    return render_template('patients.html', data1=patientdata)


@app.route('/preferences')
def patientpreferences():
    # Establish a database connection
    with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
        query2 = text('SELECT * FROM patient_preferences')

        result2 = connection.execute(query2)

        # Fetch all rows of data
        preferencedata = result2.fetchall()

    return render_template('preferences.html', data2=preferencedata)

@app.route('/demographics')
def patientdemographics():
    # Establish a database connection
    with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
        query3 = text('SELECT * FROM patient_demographics')

        result3 = connection.execute(query3)

        # Fetch all rows of data
        demographicdata = result3.fetchall()

    return render_template('demographics.html', data2=demographicdata)

if __name__ == '__main__':
    app.run(debug=True)