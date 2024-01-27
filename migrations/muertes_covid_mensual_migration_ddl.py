from sqlalchemy import Table, Column, Integer, String, MetaData
from db_connection import create_connection

# Create a connection
engine = create_connection()

# Initialize metadata
metadata = MetaData()

# Define the table
muertes_covid_mensual = Table(
   'muertes_covid_mensual', metadata, 
   Column('id', Integer, primary_key=True), 
   Column('nuevas', Integer),
   Column('poblacion', Integer),
   Column('provincia', String(100)),
   Column('total', Integer),
   Column('mes', Integer),
   Column('anio', Integer),
)

# Create the table
metadata.create_all(engine)