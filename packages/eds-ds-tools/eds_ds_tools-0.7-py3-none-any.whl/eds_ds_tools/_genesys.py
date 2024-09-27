__all__ = ['gs_query', 'gs_drop', 'gs_temp']

from ._imports import *
from ._config import config
#from ._cyberark import get_credential_both_method

class gs:
    conn = None
    @classmethod
    def get_conn(cls):
        if cls.conn is None:            
            url = "mssql+pymssql://{user}:{password}@{host}/{database}".format(
                user =  config['genesys']['user'],                   
                password = config['genesys']['password'],  
                host =  config['genesys']['host'],  
                database =  config['genesys']['database'],         
            )
            cls.conn = sqlalchemy.create_engine(url)
        return cls.conn

def gs_conn():
    return gs.get_conn()

def gs_query(q):
    return pd.read_sql(q,  gs_conn())


def gs_drop(table_name):
    try:
        gs_conn().execute(f'drop table {table_name}')
    except:
        pass

def gs_temp(df, table_name, columns_index=[]):
    gs_drop(table_name)
    df.to_sql(name=table_name, con=gs_conn(), if_exists='replace', index=False)
    for c in columns_index:
        try:
            gs_conn().execute(f'create index idx_{c} on {table_name}({c})')
        except:
            pass
    q = f'select * from {table_name}'
    return gs_query(q)

@atexit.register
def gs_close():
    if gs.conn:
        gs.conn.dispose()