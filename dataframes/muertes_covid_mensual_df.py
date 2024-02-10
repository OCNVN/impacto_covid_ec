import pandas as pd
from sqlalchemy import exc
from db_connection import create_connection

engine = create_connection()

def get_muertes_covid_mensual():
    if engine is not None:
        try:
            with engine.connect() as connection:
                df = pd.read_sql_query(
                    """
                    SELECT id, poblacion, provincia, total, anio, mes, nuevas
                    FROM muertes_covid_mensual
                    """,
                    connection
                )
                return df
        except exc.SQLAlchemyError as error:
            print ("Error while executing query", error)
        finally:
            print("PostgreSQL connection is closed")
