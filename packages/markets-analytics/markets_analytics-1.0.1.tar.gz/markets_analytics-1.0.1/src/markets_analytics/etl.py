import pandas as pd
import datetime as dt

from .connectors import redshift

class ETL:
    def get_source_count(self, schema, table, date_col, date=(dt.date.today() - pd.DateOffset(days=1)).date()):
        date = pd.to_datetime(date)
        
        query = '''
            SELECT
                COUNT(*) AS count
            FROM {}.{}
            WHERE
                {}::DATE = '{}'
        '''.format(schema, table, date_col, date)
        
        return int(redshift.execute(query, log=False).iloc[0, 0])
    
    def get_source_status(self, schema, table, date_col, date=(dt.date.today() - pd.DateOffset(days=1)).date(), threshold=0):
        return self.get_source_count(schema, table, date_col, date) > threshold
    
    def get_pipeline_runs(self, pipeline_name, date=dt.date.today()):
        query = '''
            SELECT
                COUNT(DISTINCT start_time) AS runs
            FROM sales_and_supply.pipeline_status
            WHERE
                process_name = '{}'
                AND start_time::DATE = '{}'
        '''.format(pipeline_name, date)
        
        return redshift.execute(query, log=False).iloc[0, 0]
    
    def get_pipeline_status(self, pipeline_name, date=dt.date.today()):
        query = '''
            SELECT
                status
            FROM sales_and_supply.pipeline_status
            WHERE
                process_name = '{}'
                AND start_time::DATE = '{}'
            ORDER BY start_time DESC
        '''.format(pipeline_name, date)
        
        df = redshift.execute(query, log=False)
        return df.iloc[0, 0] if len(df) > 0 else 'Not Executed Yet'
    
    def start_pipeline(self, process_name):
        df = pd.DataFrame({
            'process_name': [process_name],
            'start_time': [dt.datetime.now()],
            'end_time': [None],
            'status': ['Started'],
            'message': [None]
        })
        
        self.clean()
        redshift.insert(df, 'sales_and_supply', 'pipeline_status', log=False)
        
    def end_pipeline(self, process_name):
        query = '''
            SELECT
                *
            FROM sales_and_supply.pipeline_status
            WHERE process_name = '{}'
            QUALIFY RANK() OVER (PARTITION BY process_name ORDER BY start_time DESC) = 1
        '''.format(process_name)
        
        df = redshift.execute(query, log=False)
        
        df['end_time'] = dt.datetime.now()
        df['status'] = 'Completed'
        
        self.delete_run(process_name)
        redshift.insert(df, 'sales_and_supply', 'pipeline_status', log=False)
        
    def delete_run(self, process_name):
        query = '''
            SELECT
                start_time
            FROM sales_and_supply.pipeline_status
            WHERE process_name = '{}'
            QUALIFY RANK() OVER (PARTITION BY process_name ORDER BY start_time DESC) = 1
        '''.format(process_name)
        
        df = redshift.execute(query, log=False)
        condition = 'process_name=\'{}\' AND start_time=\'{}\' AND status=\'Started\''.format(process_name, df.iloc[0, 0])
        redshift.delete('sales_and_supply', 'pipeline_status', condition, log=False)
        
    def clean(self):
        redshift.delete('sales_and_supply', 'pipeline_status', 'start_time <= (CURRENT_DATE - INTERVAL \'30 DAY\')', log=False)
    
etl = ETL()