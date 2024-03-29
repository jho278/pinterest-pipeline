# %%
import requests
from time import time,sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
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

def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)
                # invoke url for one record, if you want to put more records replace record with records
                invoke_url = "https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0a54b96ac143-pin/record"

                #To send JSON messages you need to follow this structure
                payload = json.dumps({
                "StreamName": "streaming-0a54b96ac143-pin",
                "Data": {"index": pin_result["index"],
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
                                  "category": pin_result["category"]},
                                  "PartitionKey": "pin"
                                  })

                headers = {'Content-Type': 'application/json'}

                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print(response.status_code)
                print(response.content)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
                # Convert the timestamp to ISO format
                geo_result["timestamp"] = geo_result["timestamp"].isoformat()

                # invoke url for one record, if you want to put more records replace record with records
                invoke_url = "https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0a54b96ac143-geo/record"

                #To send JSON messages you need to follow this structure
                payload = json.dumps({
                "StreamName": "streaming-0a54b96ac143-geo",
                "Data": {"index": geo_result["ind"],
                                  "timestamp": geo_result["timestamp"], 
                                  "latitude": geo_result["latitude"], 
                                  "longitude": geo_result["longitude"],
                                  "country": geo_result["country"]},
                                  "PartitionKey": "geo"
                                })

                headers = {'Content-Type': 'application/json'}

                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print(response.status_code)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
                user_result["date_joined"] = user_result["date_joined"].isoformat()
                
                # invoke url for one record, if you want to put more records replace record with records
                invoke_url = "https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0a54b96ac143-user/record"

                #To send JSON messages you need to follow this structure
                payload = json.dumps({
                "StreamName": "streaming-0a54b96ac143-user",
                "Data": {"index": user_result["ind"],
                                  "first_name": user_result["first_name"], 
                                  "last_name": user_result["last_name"], 
                                  "age": user_result["age"],
                                  "date_joined": user_result["date_joined"]},
                                  "PartitionKey": "user"
                                  })

                headers = {'Content-Type': 'application/json'}

                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print(response.status_code)
    
            
            
#  %%
if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')

# %% 

    
    



# invoke_url = "https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/topics/0a54b96ac143.pin"  
#     #To send JSON messages you need to follow this structure
#     payload = json.dumps({
#         "records": [
#             {
#             #Data should be send as pairs of column_name:value, with different columns separated by commas       
#             "value": {"index": pin_result["index"],
#                 "unique_id": pin_result["unique_id"], 
#                 "title": pin_result["title"], 
#                 "description": pin_result["description"],
#                 "poster_name": pin_result["poster_name"],
#                 "follower_count": pin_result["follower_count"],
#                 "tag_list": pin_result["tag_list"],
#                 "is_image_or_video": pin_result["is_image_or_video"],
#                 "image_src": pin_result["image_src"],
#                 "downloaded": pin_result["downloaded"],
#                 "save_location": pin_result["save_location"],
#                 "category": pin_result["category"]}
#             }
#                 ]
#                     })

#     headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
#     response = requests.request("POST", invoke_url, headers=headers, data=payload)
            
#     print(response.status_code)
    
    



# %%
