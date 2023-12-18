import sqlite3
import pandas as pd

# Initialize the database
DATABASE = '/home/joyce_lin_1/flask_e2e_project/app/users.db'

# search for user in database
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

# get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# get values from users table
df = pd.read_sql_query("SELECT * FROM users", db)
print(df)