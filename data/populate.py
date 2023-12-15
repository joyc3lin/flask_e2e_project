import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from faker import Faker
from db import Patient, Preferences
import random

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_AZURE = os.getenv("AZURE")


# Create a database engine
engine = create_engine(DB_AZURE, echo=False)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

#create a faker instance 
fake = Faker()

#creating lists for patient data generation
sample_languages = ['English', 'Mandarin', 'Spanish', 'French', 'English', 'Korean', 'English', 'Japanese', 'English', 'Russian', 'English']

foods = ['pizza', 'pineapple', 'pasta', 'onigiri', 'ramen', 'gyro', 'cake', 'poke', 'hamburgers', 'fries', 'bbq', 'kimbap']

show = ['PhineasandFerb', 'Spongebob', 'Criminalminds', 'GoT', 'HarryPotter', 'MCU', 'GreysAnatomy', 'You', 'BlackMirror', 'OnePiece', 'DragonBallz']

hobby = ['tennis', 'drawing', 'crochet', 'sleeping', 'cooking', 'baking', 'woodworking', 'baseball', 'eating', 'skating', 'handball']

genders = ['Male', 'Female', 'Nonbinary', 'Other', 'N/A']
    
# Functions to generate fake data
def create_fake_patient():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return Patient(
        first_name = first_name,
        last_name = last_name,
        date_of_birth = fake.date_of_birth(),
        gender = random.choice(genders),
        contact_number = fake.phone_number(),
        language_spoken = random.choice(sample_languages),
        email = f"{first_name}.{last_name}@{fake.domain_name()}"
    )

def create_fake_preferences():
    return Preferences(
    patient_id = session.query(Patient).order_by(func.rand()).first().id,
    favorite_food = random.choice(foods),
    favorite_shows = random.choice(show),
    hobbies = random.choice(hobby)
    )


# Generate and insert fake data
for _ in range(20):
    fake_patient = create_fake_patient()
    session.add(fake_patient)
    

for _ in range(20):
    fake_preferences = create_fake_preferences()
    session.add(fake_preferences)

#commit
session.commit()

#close session 
session.close()