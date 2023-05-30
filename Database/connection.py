from sqlalchemy. orm import declarative_base
from sqlalchemy import create_engine
from decouple import config
from Utils.exceptions import try_except

Base = declarative_base()

password = config('keymysql')
database = config('database')
host = config('host')
user = config('user')


engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}/{database}'
)


@try_except
def run_query(statement):
    """
    This function opens a connection to the database, executes the query,
    and closes the connection.

    Returns a database object.
    """
    with engine.connect() as connection:
        consult = connection.execute(statement)
        connection.commit()
        connection.close()

    return consult
