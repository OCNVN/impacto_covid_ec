import pandas as pd
from db_connection import create_connection

# Create a connection
engine = create_connection()

# Read the CSV file
df = pd.read_csv('./data/muertes_covid_mensual.csv')

# Remove the "Table Name" column
df = df.drop(columns=['Table Names'])

# Write the DataFrame to the PostgreSQL table
df.to_sql('muertes_covid_mensual', engine, if_exists='append', index=False)