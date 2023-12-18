from flask import Flask, render_template, request, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, text
from db_functions import update_or_create_user
import logging

load_dotenv()  

AZUREURL = os.getenv("AZURE")

engine = create_engine(AZUREURL,
    connect_args={'ssl': {'ssl-mode':'preferred'}},
)    

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

logging.basicConfig(
    level=logging.DEBUG,
    filename="/home/joyce_lin_1/flask_e2e_project/logs/app.log",
    filemode="w",
    format='%(levelname)s - %(name)s - %(message)s'
)

app = Flask(__name__)   

app.secret_key = os.urandom(12)
oauth = OAuth(app)

@app.route('/')
def mainpage():
    try:
        logging.debug("success! Home page has been accessed")
        return render_template('base.html')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"    


@app.route('/google/')
def google():
    try:
        logging.debug("success! Google page has been accessed")
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        redirect_uri = url_for('google_auth', _external=True)
        print('REDIRECT URL: ', redirect_uri)
        session['nonce'] = generate_token()
        redirect_uri = 'https://5000-cs-149051346400-default.cs-us-east1-vpcf.cloudshell.dev/google/auth/'
        return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"  

@app.route('/google/auth/')
def google_auth():
    try:
        logging.debug("success! Google authorization page has been accessed")
        token = oauth.google.authorize_access_token()
        user = oauth.google.parse_id_token(token, nonce=session['nonce'])
        session['user'] = user
        update_or_create_user(user)
        print(" Google User ", user)
        return redirect('/dashboard')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"    


@app.route('/dashboard/')
def dashboard():
    try:
        logging.debug("success! Dashboard page has been accessed")
        user = session.get('user')
        if user:
            return render_template('dashboard.html', user=user)
        else:
            return redirect('/')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"    


@app.route('/logout')
def logout():
    try:
        logging.debug("successfully logged out.")
        session.pop('user', None)
        return redirect('/')
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"       



@app.route('/patients')
def patients():
    try:
        logging.debug("success! Patients page has been accessed")
    # Establish a database connection
        with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
            query1 = text('SELECT * FROM patients')

            result1 = connection.execute(query1)

        # Fetch all rows of data
            patientdata = result1.fetchall()

        return render_template('patients.html', data1=patientdata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"     
    


@app.route('/preferences')
def patientpreferences():
    try:
        logging.debug("successfully logged out.")
     # Establish a database connection
        with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
            query2 = text('SELECT * FROM patient_preferences')

            result2 = connection.execute(query2)

        # Fetch all rows of data
            preferencedata = result2.fetchall()

        return render_template('preferences.html', data2=preferencedata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"       


@app.route('/demographics')
def patientdemographics():
    try:
        logging.debug("successfully logged out.")
        # Establish a database connection
        with engine.connect() as connection:
        # Execute an SQL query to fetch data (replace this with your query)
            query3 = text('SELECT * FROM patient_demographics')

            result3 = connection.execute(query3)

        # Fetch all rows of data
            demographicdata = result3.fetchall()

        return render_template('demographics.html', data3=demographicdata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"       

if __name__ == '__main__':
    app.run(debug=False)