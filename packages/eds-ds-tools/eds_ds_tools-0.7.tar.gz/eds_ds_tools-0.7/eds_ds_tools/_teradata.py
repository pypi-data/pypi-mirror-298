__all__ = ['query_creator', 'td_query', 'td_volatile', 'td_drop_table', 'td_query_table']

from ._imports import *
from ._config import config
#from ._cyberark import get_credential_both_method

class Td:

    engine = None

    @classmethod
    def get_engine(cls):
        if cls.engine is None:            
            # udaExec = teradata.UdaExec (appName="edsds", version="1.0",logConsole=False)
            # cls.engine = udaExec.connect(method="odbc", 
            #     system=config['teradata']['system'],
            #     username= config['teradata']['user'],  
            #     password= config['teradata']['password'], 
            #     authentication="LDAP", 
            #     driver =  config['teradata']['driver']
            #     )
            user = config['teradata']['user']
            password= config['teradata']['password']
            host = config['teradata']['system']
            cls.engine = sqlalchemy.create_engine(
                 f'teradatasql://{user}:{password}@{host}/?logmech=ldap&encryptdata=true',echo=False)
        return cls.engine
    
@atexit.register
def td_close():
    if Td.engine:
        Td.engine.close()

def query_creator(table_columns='*', table_name='atuprv.dw_agreement', table_ops='sample 3'):
     q = f'select {table_columns} from {table_name} {table_ops}'
     return q
    
def td_query(q):
    return pd.read_sql(q, Td.get_engine())

def td_volatile(q, table_name):
    q = f'''
            create volatile multiset table {table_name} as (
                {q}
            ) with data
            no primary index
            on commit preserve rows;
            '''
    df = Td.get_engine().execute(q)
    return df

def td_drop_table(table_name):
    q = f'drop table {table_name};'
    try:
        Td.get_engine().execute(q)
    except:
        pass
    return

def td_query_table(database='atuprv', table=None, column=None, sample=None):
    q = f'''
        select databasename, tablename, columnname
        from dbc.columnsv
        where databasename like \'{database}\'
            {f"and tablename like '{table}'" if table else ""}
            {f"and columnname like '{column}'" if column else ""}
        {f"sample {sample}" if sample else ""}
    '''
    return td_query(q)

