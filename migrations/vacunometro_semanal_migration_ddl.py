from sqlalchemy import Table, Column, Integer, String, MetaData
from db_connection import create_connection

# Create a connection
engine = create_connection()

# Initialize metadata
metadata = MetaData()

# Define the table
vacunometro_semanal = Table(
   'vacunometro_semanal', metadata, 
   Column('id', Integer, primary_key=True),
   Column('zona', String(60)),
   Column('region', String(60)),
   Column('poblacion', Integer),
   Column('provincia', String(100)),
   Column('dosis_total', Integer),
   Column('dosis_refuerzo', Integer), 
   Column('primera_dosis', Integer), 
   Column('segunda_dosis', Integer), 
   Column('dosis_unica', Integer), 
   Column('semana', Integer),
   Column('mes', Integer),
   Column('anio', Integer),
)

# Create the table
metadata.create_all(engine)