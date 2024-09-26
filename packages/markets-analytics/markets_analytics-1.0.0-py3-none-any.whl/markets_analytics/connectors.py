import json
import pickle
import getpass
import pyexasol

import pandas as pd
import datetime as dt
import pandas_redshift as pr

from zdatalab import get_ztoken
from sqlalchemy import create_engine
from trino.auth import JWTAuthentication

class DatabaseConnector:
    def __init__(self, path='/nfs/secrets/'):
        # private variables
        self.__conn__ = None
        self.__user__ = None
        self.__host__ = None
        self.__port__ = None
        self.__dbname__ = None
        
        # public variables
        self.path = path
        
    def __init_conn__(self):
        pass
    
    def __close_conn__(self):
        pass

    def __commit__():
        pass
    
    def __str__(self):
        pass

    def test_connection(self):
        pass
        
    def execute(self, query, log=True):
        pass
    
    def insert(self, df, schema, table, append=True, log=True):
        pass
    
    def update(self, schema, table, value, condition, log=True):
        pass
    
    def delete(self, schema, table, condition=None, log=True):
        pass
    
    def truncate(self, schema, table, log=True):
        pass
    
    def create(self, ddl_query, log=True):
        pass
        
class RedshiftConnector(DatabaseConnector):
    def __init__(self, path='/nfs/secrets/', cred_file='conn_aws_cred_robot.pkl', aws_file='aws_secrets.pkl'):
        DatabaseConnector.__init__(self, path)

        self.cred_file = cred_file
        self.aws_file = aws_file
        
    def __init_conn__(self):
        with open(self.path + self.cred_file, 'rb') as fp:
            cred = pickle.load(fp)
        
        self.__user__ = cred['user']
        self.__pwd__ = cred['password']
        self.__host__ = cred['host']
        self.__port__ = cred['port']
        self.__dbname__ = cred['dbname']
        
        self.__conn__ = create_engine('redshift+psycopg2://{}:{}@{}:{}/{}'
            .format(self.__user__, self.__pwd__, self.__host__, self.__port__, self.__dbname__))
        
    def __close_conn__(self):
        self.__conn__.dispose()
        
    def __commit__(self, query):
        self.__init_conn__()
        conn = self.__conn__.raw_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        self.__close_conn__()
        
    def __str__(self):
        if self.__user__ is None:
            return 'No connection has been made to any Redshift instance'
        return 'Username `{}` connected to Redshift host: {}:{}'.format(self.__user__, self.__host__, self.__port__)
        
    def test_connection(self):
        self.__init_conn__()
        print(self)
        self.__close_conn__()

    def execute(self, query, log=True):
        if log: print('[{}] Executing Query'.format(dt.datetime.now()))
        
        self.__init_conn__()
        df = pd.read_sql_query(query, self.__conn__)
        self.__close_conn__()
        
        if log: print('[{}] Query Executed Successfully'.format(dt.datetime.now()))
        return df
    
    def insert(self, df, schema, table, append=True, log=True):
        if log: print('[{}] Inserting data to {}.{}'.format(dt.datetime.now(), schema, table))
        
        self.__init_conn__()

        with open(self.path + self.aws_file, 'rb') as fp:
            aws_secrets = pickle.load(fp)
            
        pr.connect_to_redshift(
            dbname = self.__dbname__,
            host = self.__host__,
            port = self.__port__,
            user = self.__user__,
            password = self.__pwd__
        )

        pr.connect_to_s3(
            aws_access_key_id = aws_secrets['aws_access_key_id'],
            aws_secret_access_key = aws_secrets['aws_secret_access_key'],
            bucket = 'sales-supply-analytics',
            subdirectory = None
        )

        pr.pandas_to_redshift(
            data_frame = df,
            redshift_table_name = '{}.{}'.format(schema, table), 
            verbose = False, 
            append = append
        )
        
        if log: print('[{}] Data Inserted Successfully'.format(dt.datetime.now()))
      
    def update(self, schema, table, value, condition, log=True):
        if log: print('[{}] Updating data for {}.{}'.format(dt.datetime.now(), schema, table))
        
        query = '''
            UPDATE {}.{}
            SET {}
            WHERE {}
        '''.format(schema, table, value, condition)

        self.__commit__(query)
        if log: print('[{}] Updated Data Successfully'.format(dt.datetime.now()))
    
    def delete(self, schema, table, condition=None, log=True):
        if log: print('[{}] Deleting data from {}.{}'.format(dt.datetime.now(), schema, table))
        
        if condition == None:
            self.truncate(schema, table)
        else:
            query = '''
                DELETE FROM {}.{}
                WHERE
                    {}
            '''.format(schema, table, condition)

            self.__commit__(query)
            if log: print('[{}] Deleted Data Successfully'.format(dt.datetime.now()))
        
    def truncate(self, schema, table, log=True):
        if log: print('[{}] Truncating table {}.{}'.format(dt.datetime.now(), schema, table))
        
        query = '''
            TRUNCATE TABLE {}.{}
        '''.format(schema, table)
    
        self.__commit__(query)
        if log: print('[{}] Data Truncated Successfully'.format(dt.datetime.now()))
        
    def create(self, ddl_query, log=True):
        if log: print('[{}] Creating Table'.format(dt.datetime.now()))
        
        self.__commit__(ddl_query)
        if log: print('[{}] Table Created Successfully'.format(dt.datetime.now()))
        
class DatalakeConnector(DatabaseConnector):
    def __init__(self, path=None):
        DatabaseConnector.__init__(self, path)
        
    def __init_conn__(self):
        self.__user__ = getpass.getuser()
        self.__pwd__ = get_ztoken()
        self.__host__ = 'interactive.starburst.zalando.net'
        self.__port__ = 443
        self.__dbname__ = 'hive'
        
        self.__conn__ = create_engine(
            'trino://{}@{}:{}/{}'.format(self.__user__, self.__host__, self.__port__, self.__dbname__),
            connect_args={
                 'auth': JWTAuthentication(self.__pwd__),
                 'http_scheme': 'https',
            },
        )
        
    def __close_conn__(self):
        self.__conn__.dispose()
        
    def __str__(self):
        if self.__user__ is None:
            return 'No connection has been made to any Datalake instance'
        return 'Username `{}` connected to Datalake host: {}:{}'.format(self.__user__, self.__host__, self.__port__)
        
    def test_connection(self):
        self.__init_conn__()
        print(self)
        self.__close_conn__()

    def execute(self, query, log=True):
        if log: print('[{}] Executing Query'.format(dt.datetime.now()))
        
        self.__init_conn__()
        df = pd.read_sql_query(query, self.__conn__)
        self.__close_conn__()
        
        if log: print('[{}] Query Executed Successfully'.format(dt.datetime.now()))
        return df
    
class ExasolConnector(DatabaseConnector):
    def __init__(self, path='/nfs/secrets/'):
        DatabaseConnector.__init__(self, path)
        
    def __init_conn__(self):
        with open(self.path + 'exasol_conn.json', 'rb') as fp:
            cred = json.load(fp)
        
        self.__user__ = cred['username']
        self.__pwd__ = cred['password']
        self.__host__ = cred['host']
        self.__port__ = cred['port']
        self.__dbname__ = None
        
        dsn = "{}:{}".format(self.__host__, self.__port__)
        self.__conn__ = pyexasol.connect(dsn=dsn, user=self.__user__, password=self.__pwd__, compression=True)
        
    def __close_conn__(self):
        self.__conn__.close()
        
    def __str__(self):
        if self.__user__ is None:
            return 'No connection has been made to any Exasol instance'
        return 'Username `{}` connected to Exasol host: {}:{}'.format(self.__user__, self.__host__, self.__port__)
        
    def test_connection(self):
        self.__init_conn__()
        print(self)
        self.__close_conn__()

    def execute(self, query, log=True):
        if log: print('[{}] Executing Query'.format(dt.datetime.now()))
        
        self.__init_conn__()
        df = self.__conn__.export_to_pandas(query)
        self.__close_conn__()
        
        if log: print('[{}] Query Executed Successfully'.format(dt.datetime.now()))
        return df
    
redshift = RedshiftConnector()
datalake = DatalakeConnector()
exasol = ExasolConnector()