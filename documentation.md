# Creating conda environment
download miniconda
activate test environment in anaconda command prompt
create new terminal in vs code 

miniconda should be activated at this point
conda create --name <name>
conda info -envs
conda activate <name>

# installing packages
conda install <package>project

# What data services are used on AWS?
- EC2
- S3
- IAM management

# Configure an Amazon EC2 instance to use as an Apache Kafka client machine
# Create a .pem file locally
- A key pair file ending in .pem allows the user to connect to their EC2 instance. The content of the key pair is found in the Parameter store.
- Within the SSH client, navigate to the home directory (cd ~) and save the .pem file in this directory. Ensure the file is publicly unviewable then connect the instance via its public DNS. Use code below
- chmod 400 key-pair.pem. This must be stored in wsl directory

# Connect to the EC2 instance
- Instructions are given in the AWS EC2 instance to connect. In this project we connect via SSH (WSL Ubuntu)
- Run this code within the home directory (cd ~): ssh -i 0a54b96ac143-key-pair.pem ec2-user@ec2-34-235-131-58.compute-1.amazonaws.com

# Set up Kafka on the EC2 instance
- The project provides an IAM authenticated MSK cluster. As a reminder, MSK stands for managed streaming for Apache Kafka and uses Kafka to process data and simplifies the challenges in setup, scale and manage in production. 

# Install packages to run Kafka on the EC2 client machine.
- Three packages: Java-1.8.0, Kafka_2.12-2.8.1, AWS MSK IAM authenticator.
- The MSK cluster requires AWS IAM to authorise users for production to the cluster, hence the need for the last package above. 
- Set the CLASSPATH environment variable. This stores the location of the jar file (msk authenticator) and ensures it is accessible regardless of the location where user runs commands. 
- Add this environment variable to the ~/.bashrc to automate the above process so it doesnt reset each time a new session/new EC2 instance is run

# Assume the ec2-access-role
- To ensure necessary permissions to authenticate MSK cluster, the user needs to configure the Roles within AWS IAM console.
- This involves adding the IAM role as a principal type in the trust relationships and ensuring the ARN matches with the ec2-access-role. 

# Configure kafka client to use AWS authentication to use the cluster. 
- Configure the client.properties file within the kafka/bin folder such as using the user's access role in the awsRoleArn parameter. 

# Create kafka topics
- Within the Kafka/bin folder in the EC2 instance, run the following command:
- ./kafka-topics.sh --bootstrap-server BootstrapServerString --command-config client.properties --create --topic <topic_name>
- Replace the Bootstrap server string with the link below.
- Three topics were created: 0a54b96ac143.pin, 0a54b96ac143.geo, 0a54b96ac143.user

IAM role: arn:aws:iam::584739742957:role/0a54b96ac143-ec2-access-role

bootstrap server string: b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098

plaintext Apache Zookeeper connection string: z-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181

# Create topic 
./kafka-topics.sh --bootstrap-server b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 0a54b96ac143.pin

repeat for geo and user

# Batch processing: Connecting a MSK cluster to a S3 bucket.
- Use MSK Connect to connect the MSK cluster to a S3 bucket

# S3 bucket name
- A S3 bucket, IAM role to write to this bucket and a VPC Endpoint to S3 are created for this project.
- user-0a54b96ac143-bucket
- The IAM role can have actions that enable the user to list, delete and get the location of said bucket. The role enables necessary permissions to write to destination bucket. 
- The VPC endpoint is a virtual private cloud

# Connect EC2 to S3. then create plugin
- A plugin will contain the code that defines the logic of our connector. This requires downloading Confluent.io Amazon S3 connector. This connector is a sink connector that exports data from kafka topics to S3 objects in either JSON, Avro or Bytes format
- In the EC2 instance, download the above within a folder called kafka-connect-s3. Copy the connector to the S3 bucket 
- aws s3 cp ./confluentinc-kafka-connect-s3-10.0.3.zip s3://<BUCKET_NAME>/kafka-connect-s3/ - After runnning this code, you should see it in the S3 AWS.
- Within MSK Connector, create custom plugin and select the ZIP file within the S3 bucket as the S3 url. 

# Create connector
- Within MSK Connect, create connector. Select plugin created from above and configure the settings. topics.regex == user-id, s3.bucket.name = bucket.  selecting the EC2-iam-ec2-access
- After creating both plugin and connector, should be able to send data from MSK to S3.

# To replicate Pinterest's experimental data pipeline, an API is needed to send data to the MSK cluster, which in turn stores it in an S3 bucket using the connector. 
- The Kafka REST Proxy integration provides a RESTful interface to a Kafka cluster. This enables simple produce and consume of messages.

# Create REST proxy API
- Standard for client-server communication. REST APIs have higher latency rate than HTTP APIs which is bad. However, they have full endpoint support, can be edge-optimised and supports regional and private endpoints.
- A proxy integration provide the selected integration access to many resources and features at once, without specifiying multiple resource paths using the greedy parameter {proxy+}
- Consider an API with the following resource paths:
    - car/{type}/{subtype}/{parts}
    - car/{type}/{subtype}/{colour}
    - car/{type}/{subtype}/{colour}/{cost}
- Tedious to specify these paths individually. With the proxy resource, you can provide your integration with access to all available resources. 
- When integration is created and configured, you can access method execution. This shows execution order of the methods. There are four steps:
    - Method request: step used to configure security settings (API keys), query-string parameters and request headers
    - integration request: The gateway makes a request to the integration, passing along request data and transforming if necessary
    - Integration response: Result from the backend. Results are transformed if required and sent to the method response
    - Method response: Contains output of the API and served to user. Usually contains HTTP status code, headers and a body. 

# Deploy API
- Make note of the invoke url

# invoke api url
https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/topics/0a54b96ac143.pin

# topic names 
0a54b96ac143.pin
0a54b96ac143.geo
0a54b96ac143.user

# Kafka REST Proxy integration type set to HTTP
- HTTP proxy integration is a good way of building APIs enabling web applications to access multiple resources on the integrated HTTP endpoint. API Gateway passes client-submitted method requests to the backend and in turn the backend parses th eincoming data request to determine the return responses.
- The endpoint URL should be set to the Kafka client amazon EC2 instance publicDNS, found in the EC2 console.

# endpoint url
http://ec2-34-235-131-58.compute-1.amazonaws.com:8082/{proxy}

# Starting REST proxy within the confluent bin folder
- To consume data using MSK from the API created, additional packages are required in the client EC2 machine to communicate with the MSK cluster.
- To configure the REST proxy to communicate with desired MSK cluster and to perform IAM authentication, you need to configure the kafka-rest.properties file.
- add the bootstrap.server and zookeeper.connect variables in the file and ensure it matches with the strings in the MSK cluster.
- Add the IAM MSK authentication package by adding the relevant code to the kafka-rest.properties file
- This is slightly different to the kafka client.properties. as all configurations should be pre-fixed with client to enable communication between REST proxy and cluser brokers. 
- Within the confluent/bin folder, run the below command
- ./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties

# invoke api url
- After deploying the API, make note of the invoke URL. The external kafka REST proxy exposed via API gateway is below. This url is used to send messages through API gateway into the user's consumer
https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/topics/0a54b96ac143.pin

# API testing
import requests
import json

example_df = {"index": 1, "name": "Maya", "age": 25, "role": "engineer"}

invoke_url = "https://YourAPIInvokeURL/YourDeploymentStage/topics/YourTopicName"
#To send JSON messages you need to follow this structure
payload = json.dumps({
    "records": [
        {
        #Data should be send as pairs of column_name:value, with different columns separated by commas       
        "value": {"index": example_df["index"], "name": example_df["name"], "age": example_df["age"], "role": example_df["role"]}
        }
    ]
})

headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
response = requests.request("POST", invoke_url, headers=headers, data=payload)
# Git
Create git repository on github and copy url
git init
git remote add origin (url)


