"""

pip install sqlalchemy alembic mysql-connector-python
pip install pymysql

"""

## Part 1 - Define SQLAlchemy models for patients and their preferences:

from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

AZUREURL = os.getenv("AZURE")

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact_number = Column(String(100))
    email = Column(String(100))
    address = Column(String(200))

    preferences = relationship('Preferences', back_populates='patient')
    demographics = relationship('Demographics', back_populates='patient2')

class Preferences(Base):
    __tablename__ = 'patient_preferences'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    favorite_food = Column(String(200), nullable=False)
    favorite_shows = Column(String(200))
    hobbies = Column(String(200))
    toothpaste_flavor = Column(String(100))  
    
    patient = relationship('Patient', back_populates='preferences')

class Demographics(Base):
    __tablename__ = 'patient_demographics'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    gender = Column(String(10), nullable=False)
    language_spoken = Column(String(100))
    marital_status = Column(String(100))
    nationality = Column(String(100))
    occupation = Column(String(100))

    patient2 = relationship('Patient', back_populates='demographics')

### Part 2 - initial sqlalchemy-engine to connect to db:

engine = create_engine(AZUREURL,
    connect_args={'ssl': {'ssl-mode':'preferred'}},
)    


## Test connection

inspector = inspect(engine)
inspector.get_table_names()


### Part 3 - create the tables using sqlalchemy models, with no raw SQL required:

Base.metadata.create_all(engine)