import requests
from time import time,sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from func_timeout import func_timeout, FunctionTimedOut
import yaml



random.seed(100)


class AWSDBConnector:

    def __init__(self):
        pass
    
    def read_db_creds(self):
        with open('cred.yaml','r') as file:
            self.credentials = yaml.safe_load(file)
        return self.credentials
        
    def create_db_connector(self):
        self.read_db_creds()
        HOST = self.credentials['HOST']
        USER = self.credentials['USER']
        PASSWORD = self.credentials['PASSWORD']
        DATABASE = self.credentials['DATABASE']
        PORT = self.credentials['PORT']
        
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def timeout_decorator(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except FunctionTimedOut:
                print(f"{func.__name__} took longer than {seconds} seconds and has been terminated.")
                return None

        return wrapper

    return decorator

@timeout_decorator(30)
def run_infinite_post_data_loop(duration = 30):
    start_time = time()
    while time()-start_time < duration:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            print(pin_result)
            print(geo_result)
            print(user_result)
            
            

#%%
if __name__ == "__main__":
    from user_posting_emulation import run_infinite_post_data_loop
    run_infinite_post_data_loop()
    print('Working')
    
#%% # Code chunk to identify tables in the AWS store
if __name__ == "__main__":
    from sqlalchemy import inspect
    from user_posting_emulation import AWSDBConnector
    new_connector = AWSDBConnector()
    db_engine = new_connector.create_db_connector()
    inspector = inspect(db_engine)
    tables = inspector.get_table_names()
    # Print the available tables
    print("Available Tables:")
    for table_name in tables:
        print(table_name)
    # Remember to close the connection after use
    db_engine.dispose()

# %% # Code chunk to view first 10 rows of pinterest_data
if __name__ == "__main__":
    from sqlalchemy import text
    from user_posting_emulation import AWSDBConnector
    new_connector = AWSDBConnector()
    db_engine = new_connector.create_db_connector()
    
    with db_engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM geolocation_data LIMIT 10"))
        for row in result:
            print(row)

# %%
if __name__ == "__main__":
    import pandas as pd
    from user_posting_emulation import AWSDBConnector
    new_connector = AWSDBConnector()
    db_engine = new_connector.create_db_connector()
    
    location = pd.read_sql_query('''SELECT * FROM geolocation_data LIMIT 10''',db_engine)
    print(location)
    
    user = pd.read_sql_table('user_data',db_engine)
    print(user.columns) 
    print(user.head(10))

# %%
