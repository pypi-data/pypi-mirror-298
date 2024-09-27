__all__ = ['pc_query', 'pc_drop', 'pc_temp']

from ._imports import *
from ._config import config
#from ._cyberark import get_credential_both_method

class Pc:

    conn = None

    @classmethod
    def get_conn(cls):
        if cls.conn is None:
            # user, password = get_credential_both_method('policycenter')
            url = "mssql+pymssql://{user}:{password}@{host}/{database}".format(
                user = config['policycenter']['user'], 
                password = config['policycenter']['password'],  
                host =  config['policycenter']['host'],  
                database = config['policycenter']['database'],  
            )
            cls.conn = sqlalchemy.create_engine(url)
        return cls.conn

def pc_conn():
    return Pc.get_conn()

def pc_query(q):
    return pd.read_sql(q, pc_conn())

def pc_drop(table_name):
    try:
        pc_conn().execute(f'drop table {table_name}')
    except:
        pass

def pc_temp(df, table_name):
    pc_drop(table_name)
    df.to_sql(name=table_name, con=pc_conn(), index=False)
    q = f'select * from {table_name}'
    return pc_query(q)

@atexit.register
def pc_close():
    if Pc.conn:
        Pc.conn.dispose()
