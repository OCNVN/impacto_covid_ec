import pandas as pd
from sqlalchemy import exc
from db_connection import create_connection

engine = create_connection()

def get_defunciones_mensual():
    if engine is not None:
        try:
            with engine.connect() as connection:
                df = pd.read_sql_query(
                    """
                    SELECT id, acumuladas, poblacion, provincia, total, mes, anio, 
                        (TO_DATE(anio || '-' || mes , 'YYYY-MM')::date) as fecha,
                        EXTRACT(EPOCH FROM(TO_DATE(anio || '-' || mes , 'YYYY-MM')::date)) AS timestamp
                    FROM defunciones_mensual
                    ORDER BY fecha
                    """,
                    connection
                )
                return df
        except exc.SQLAlchemyError as error:
            print ("Error while executing query", error)
        finally:
            print("PostgreSQL connection is closed")
