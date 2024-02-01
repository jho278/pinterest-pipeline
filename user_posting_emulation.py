import requests
from time import time,sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
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
def run_infinite_post_data_loop(duration = 5):
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

            invoke_url = "https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/topics/0a54b96ac143.pin"
            #To send JSON messages you need to follow this structure
            payload = json.dumps({
                "records": [
                {
            #Data should be send as pairs of column_name:value, with different columns separated by commas       
                "value": {"index": pin_result["index"],
                          "unique_id": pin_result["unique_id"], 
                          "title": pin_result["title"], 
                          "description": pin_result["description"],
                          "poster_name": pin_result["poster_name"],
                          "follower_count": pin_result["follower_count"],
                          "tag_list": pin_result["tag_list"],
                          "is_image_or_video": pin_result["is_image_or_video"],
                          "image_src": pin_result["image_src"],
                          "downloaded": pin_result["downloaded"],
                          "save_location": pin_result["save_location"],
                          "category": pin_result["category"]}
                }
                         ]
                                })

            headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
            response = requests.request("POST", invoke_url, headers=headers, data=payload)
            
            print(response.status_code)
            


if __name__ == "__main__":
    from user_posting_emulation import run_infinite_post_data_loop
    run_infinite_post_data_loop()
    print('Working')
    
    


