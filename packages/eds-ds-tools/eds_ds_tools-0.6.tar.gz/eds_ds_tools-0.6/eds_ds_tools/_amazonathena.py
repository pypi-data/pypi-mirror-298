__all__ = [
    'athena_query',
]

from ._imports import *
from ._config import config
from ._amazons3 import *
#from ._cyberark import *

class AmazonAthena:
    clients = {}

    @classmethod
    def get_client(cls, env):
        if env not in cls.clients:
            if config.has_option(f'aws_{env}','aws_session_token'):
                cls.clients[env] = boto3.client(
                    service_name            = 'athena',
                    region_name             = config[f'aws_{env}']['region'], 
                    aws_access_key_id       = config[f'aws_{env}']['aws_access_key_id'],
                    aws_secret_access_key   = config[f'aws_{env}']['aws_secret_access_key'],
                    aws_session_token       = config[f'aws_{env}']['aws_session_token']
                )
            else:
                #aws_access_key_id, aws_secret_access_key  = get_credential_both_method(f'aws_{env}')
                cls.clients[env] = boto3.client(
                    service_name            = 'athena',
                    region_name             = config[f'aws_{env}']['region'], 
                    aws_access_key_id       = config[f'aws_{env}']['aws_access_key_id'],
                    aws_secret_access_key   = config[f'aws_{env}']['aws_secret_access_key'],
                    # aws_access_key_id  = aws_access_key_id,
                    # aws_secret_access_key  = aws_secret_access_key 
                )
        return cls.clients[env]

def client(env):
    return AmazonAthena.get_client(env)

@atexit.register
def athena_close():
    for client in AmazonAthena.clients.values():
        client.close()

def athena_query(query, env='dl', path=None, cleanup=False, time_sleep=1, max_execution=100):
    path = config[f'aws_{env}']['aws_folder'] if path is None else path
    params = {
        'env':       env,
        'region':    config[f'aws_{env}']['region'],
        'bucket':    config[f'aws_{env}']['bucket'],
        'database':  'amica_eds_digital',
        'workgroup': 'primary',
        'path':      path,
        'query':     query,
    }

    athena_client = client(env)
    execution = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': params['database']
        },
        ResultConfiguration={
            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path']
        }
    )
    execution_id = execution['QueryExecutionId']

    state = 'RUNNING'
    while max_execution > 0 and state in ['RUNNING', 'QUEUED']:
        max_execution = max_execution - 1
        response = athena_client.get_query_execution(QueryExecutionId=execution_id)

        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']

            if state == 'FAILED':
                raise Exception('Athena Query Failed')
            elif state == 'SUCCEEDED':
                s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                filename = re.findall('.*\/(.*)', s3_path)[0]

                s3_file_path = os.path.join(path, filename)
                df = s3_download_and_read_csv(s3_file_path, s3_bucket=params['bucket'], env=env)
                if cleanup:
                    s3_delete_file(s3_file_path, s3_bucket=params['bucket'], env=env)
                return df
        time.sleep(time_sleep)
