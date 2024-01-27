import pandas as pd
from db_connection import create_connection

# Create a connection
engine = create_connection()

# Read the CSV file
df = pd.read_csv('./data/positivas_semanal.csv')

# Remove the "lat", "lng" columns
df = df.drop(columns=['lat', 'lng'])

# Write the DataFrame to the PostgreSQL table
df.to_sql('positivas_semanal', engine, if_exists='append', index=False)