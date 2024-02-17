import pandas as pd
from sqlalchemy import exc
from db_connection import create_connection

engine = create_connection()

def get_vacunometro_semanal():
    if engine is not None:
        try:
            with engine.connect() as connection:
                df = pd.read_sql_query(
                    """
                    SELECT id, poblacion, provincia, anio, mes, dosis_refuerzo, dosis_total, dosis_unica, primera_dosis, segunda_dosis, region, zona, semana,
                        (TO_DATE(anio || '-' || semana , 'YYYY-WW')::date) as fecha,
                        EXTRACT(EPOCH FROM(TO_DATE(anio || '-' || semana , 'YYYY-WW')::date)) AS timestamp
                    FROM vacunometro_semanal
                    ORDER BY fecha
                    """,
                    connection
                )

                # Rows for the same week number are split when the month changes, so we need to group by fecha and province
                df = df.groupby(['fecha', 'provincia']).agg({
                    'dosis_refuerzo': 'sum',
                    'dosis_total': 'sum',
                    'dosis_unica': 'sum',
                    'primera_dosis': 'sum',
                    'segunda_dosis': 'sum',
                    'id': 'first',
                    'poblacion': 'first',
                    'region': 'first',
                    'zona': 'first',
                    'semana': 'first',
                    'anio': 'first',
                    'mes': 'first',
                    'timestamp': 'first'
                }).reset_index()

                return df
        except exc.SQLAlchemyError as error:
            print ("Error while executing query", error)
        finally:
            print("PostgreSQL connection is closed")
