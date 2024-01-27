import pandas as pd
from db_connection import create_connection

# Create a connection
engine = create_connection()

# Read the CSV file
df = pd.read_csv('./data/defunciones_semanal.csv')

# Write the DataFrame to the PostgreSQL table
df.to_sql('defunciones_semanal', engine, if_exists='append', index=False)