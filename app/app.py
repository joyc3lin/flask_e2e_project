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

AZUREURL = 'mysql+pymysql://joyce:Pineapple!1@joycefinal.mysql.database.azure.com/joyce'

engine = create_engine(AZUREURL,
    connect_args={'ssl': {'ssl-mode':'preferred'}},
)    

GOOGLE_CLIENT_ID = '60644915922-f57nr7v0vh2ck6qkslaorskcuv035q98.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

logging.basicConfig(
    level=logging.DEBUG,
    filename="logs/app.log",
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
        id = request.args.get('id')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        date_of_birth = request.args.get('date_of_birth')
        contact_number = request.args.get('contact_number')
        email = request.args.get('email')
        address = request.args.get('address')
    # Establish a database connection
        with engine.connect() as connection:
            if first_name:
                query1 = text('SELECT * FROM patients WHERE first_name = :first_name')
                result1 = connection.execute(query1, {"first_name": first_name})
            elif last_name:
                query1 = text('SELECT * FROM patients WHERE last_name = :last_name')
                result1 = connection.execute(query1, {"last_name": last_name})
            elif id:
                query1 = text('SELECT * FROM patients WHERE id = :id')
                result1 = connection.execute(query1, {"id": id})
            elif date_of_birth:
                query1 = text('SELECT * FROM patients WHERE date_of_birth = :date_of_birth')
                result1 = connection.execute(query1, {"date_of_birth": date_of_birth})
            elif contact_number:
                query1 = text('SELECT * FROM patients WHERE contact_number = :contact_number')
                result1 = connection.execute(query1, {"contact_number": contact_number})
            elif email:
                query1 = text('SELECT * FROM patients WHERE email = :email')
                result1 = connection.execute(query1, {"email": email})
            elif address:
                query1 = text('SELECT * FROM patients WHERE address = :address')
                result1 = connection.execute(query1, {"address": address})
            else:
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
        logging.debug("success! Preferences page has been accessed")
        id = request.args.get('id')
        patient_id = request.args.get('patient_id')
        favorite_food = request.args.get('favorite_food')
        favorite_shows = request.args.get('favorite_shows')
        hobbies = request.args.get('hobbies')
        toothpaste_flavor = request.args.get('toothpaste_flavor') 
     # Establish a database connection
        with engine.connect() as connection:
            if id:
                query2 = text('SELECT * FROM patient_preferences WHERE id = :id')
                result2 = connection.execute(query2, {"id": id})
            elif patient_id:
                query2 = text('SELECT * FROM patient_preferences WHERE patient_id = :patient_id')
                result2 = connection.execute(query2, {"patient_id": patient_id})
            elif favorite_food:
                query2 = text('SELECT * FROM patient_preferences WHERE favorite_food = :favorite_food')
                result2 = connection.execute(query2, {"favorite_food": favorite_food})
            elif favorite_shows:
                query2 = text('SELECT * FROM patient_preferences WHERE favorite_shows = :favorite_shows')
                result2 = connection.execute(query2, {"favorite_shows": favorite_shows})
            elif hobbies:
                query2 = text('SELECT * FROM patient_preferences WHERE hobbies = :hobbies')
                result2 = connection.execute(query2, {"hobbies": hobbies})
            elif toothpaste_flavor:
                query2 = text('SELECT * FROM patient_preferences WHERE toothpaste_flavor = :toothpaste_flavor')
                result2 = connection.execute(query2, {"toothpaste_flavor": toothpaste_flavor})
            else:
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
        logging.debug("success! Demographics page has been accessed")
        id = request.args.get('id')
        patient_id = request.args.get('patient_id')
        gender = request.args.get('gender')
        language_spoken = request.args.get('language_spoken')
        marital_status = request.args.get('marital_status')
        nationality = request.args.get('nationality')
        occupation = request.args.get('occupation')
        # Establish a database connection
        with engine.connect() as connection:
            if id:
                query3 = text('SELECT * FROM patient_demographics WHERE id = :id')
                result3 = connection.execute(query3, {"id": id})
            elif patient_id:
                query3 = text('SELECT * FROM patient_demographics WHERE patient_id = :patient_id')
                result3 = connection.execute(query3, {"patient_id": patient_id})
            elif gender:
                query3 = text('SELECT * FROM patient_demographics WHERE gender = :gender')
                result3 = connection.execute(query3, {"gender": gender})
            elif language_spoken:
                query3 = text('SELECT * FROM patient_demographics WHERE language_spoken = :language_spoken')
                result3 = connection.execute(query3, {"language_spoken": language_spoken})
            elif marital_status:
                query3 = text('SELECT * FROM patient_demographics WHERE marital_status = :marital_status')
                result3 = connection.execute(query3, {"marital_status": marital_status})
            elif nationality:
                query3 = text('SELECT * FROM patient_demographics WHERE nationality = :nationality')
                result3 = connection.execute(query3, {"nationality": nationality})
            elif occupation:
                query3 = text('SELECT * FROM patient_demographics WHERE occupation = :occupation')
                result3 = connection.execute(query3, {"occupation": occupation})
            else:
                query3 = text('SELECT * FROM patient_demographics')
                result3 = connection.execute(query3)   

        # Fetch all rows of data
            demographicdata = result3.fetchall()

        return render_template('demographics.html', data3=demographicdata)
    except Exception as e:
        logging.error(f"an error occured! {e}")
        return "try again"       

if __name__ == '__main__':
    app.run(debug=False, port=8080, host='0.0.0.0')