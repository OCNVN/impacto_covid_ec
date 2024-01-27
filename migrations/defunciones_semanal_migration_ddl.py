from sqlalchemy import Table, Column, Integer, String, MetaData
from db_connection import create_connection

# Create a connection
engine = create_connection()

# Initialize metadata
metadata = MetaData()

# Define the table
defunciones_semanal = Table(
   'defunciones_semanal', metadata, 
   Column('id', Integer, primary_key=True), 
   Column('acumuladas', Integer),
   Column('poblacion', Integer),
   Column('provincia', String(100)),
   Column('total', Integer),
   Column('semana', Integer),
   Column('anio', Integer),
)

# Create the table
metadata.create_all(engine)