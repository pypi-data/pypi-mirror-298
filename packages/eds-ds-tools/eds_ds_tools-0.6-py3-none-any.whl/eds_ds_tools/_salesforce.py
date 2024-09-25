__all__ = ['sf_query']

from ._imports import *
from ._config import config
from sys import platform
#from ._cyberark import get_credential_both_method

class sf:

    conn = None

    @classmethod
    def query(cls, q):
        if cls.conn is None:
            # user, password = get_credential_both_method('salesforce')
            if platform == "linux" or platform == "linux2":
                sslrootcert = config['salesforce']['linux_sslrootcert']
                sslcert     = config['salesforce']['linux_sslcert']
                sslkey      = config['salesforce']['linux_sslkey'] 
            elif platform == "win32":
                sslrootcert = config['salesforce']['sslrootcert']
                sslcert     = config['salesforce']['sslcert']
                sslkey      = config['salesforce']['sslkey'] 


            cls.conn = psycopg2.connect(
                dbname      =  config['salesforce']['dbname'],  
                user        = config['salesforce']['user'],
                password    = config['salesforce']['password'],               
                host        = config['salesforce']['host'], 
                port        = 5432,
                sslmode     = 'require',
                sslrootcert = sslrootcert,
                sslcert     = sslcert,
                sslkey      = sslkey,            
            )
        return pd.read_sql(q, cls.conn)

def sf_query(q):
    return sf.query(q)

@atexit.register
def sf_close():
    if sf.conn:        
        sf.conn.close()