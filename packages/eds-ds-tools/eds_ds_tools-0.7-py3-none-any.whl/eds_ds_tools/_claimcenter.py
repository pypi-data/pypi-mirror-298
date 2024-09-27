__all__ = ['cc_query', 'cc_query_table']

from ._imports import *
from ._config import config
#from ._cyberark import get_credential_both_method

class Cc:

    conn = None

    @classmethod
    def query(cls, q):
        if cls.conn is None:            
            url = "postgresql+psycopg2://{user}:{password}@{host}/{database}".format(
                user = config['claimcenter']['user'], 
                password =  config['claimcenter']['password'], 
                host = config['claimcenter']['host'],  
                database = config['claimcenter']['database']  
            )
            cls.conn = sqlalchemy.create_engine(url)
        return pd.read_sql(q, cls.conn)
  
def cc_query(q):
    return Cc.query(q)

def cc_query_table(database='cc_merge', table=None, column=None, limit=None):
    q = f'''
        select table_schema, table_name, column_name
        from information_schema.columns
        where table_schema like \'{database}\'
            {f"and table_name like '{table}'" if table else ""}
            {f"and column_name like '{column}'" if column else ""}
        {f"limit {limit}" if limit else ""}
    '''
    return cc_query(q)

@atexit.register
def cc_close():
    if Cc.conn:
        # Cc.conn.close()
        Cc.conn.dispose()