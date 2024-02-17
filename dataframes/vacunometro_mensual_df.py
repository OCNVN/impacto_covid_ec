import pandas as pd
from sqlalchemy import exc
from db_connection import create_connection

engine = create_connection()

def get_vacunometro_mensual():
    if engine is not None:
        try:
            with engine.connect() as connection:
                df = pd.read_sql_query(
                    """
                    SELECT id, poblacion, provincia, anio, mes, dosis_refuerzo, dosis_total, dosis_unica, primera_dosis, region, zona,
                        (TO_DATE(anio || '-' || mes , 'YYYY-MM')::date) as fecha,
                        EXTRACT(EPOCH FROM(TO_DATE(anio || '-' || mes , 'YYYY-MM')::date)) AS timestamp
                    FROM vacunometro_mensual
                    ORDER BY fecha
                    """,
                    connection
                )
                return df
        except exc.SQLAlchemyError as error:
            print ("Error while executing query", error)
        finally:
            print("PostgreSQL connection is closed")
