# Emulation of the Pinterest data pipeline
For my final project with AICore, I will emulate the data pipeline for the Pinterest posts using a combination of AWS, Databricks and Python in VS Code. I aim to develop a workflow covering: 
- Data ingestion of the Pinterest data into AWS via Apache Kafka in an EC2 instance. 
- Data storage of the Pinterest data in a S3 object. 
- Mounting the S3 storage in Databricks for transformation and analysis. 

I will have demonstrated the application of my knowledge in AWS by processing data in real-time and creating a workflow to analyse the data to inform my stakeholders and provide analysis to support decision-making. 


## Installation Instructions - Batch processing
### C2 instance
- Set up EC2 instance on client machine (within AWS) and configure to run MSK cluster (Apache Kafka client machine). 
- Within EC2 client machine, install 3 packages: Java-1.8.0, Kafka_2.12-2.8.1, AWS MSK IAM authenticator. The authenticator authorises users for production to the cluster. 
- Set the CLASSPATH environment variable in the ~/.bashrc to automate location of the JAR file (authenticator)
- Configure permissions in AWS IAM roles. This includes adding principal type in trust relationship, ensuring ARN matches with ec2-access-role
- You should now be able to connect to the EC2 instance and run Kafka. 

### Kafka topics
- Events are organised and stored in a Kafka topic. A topic is analogous to a folder in a filesystem, and the events are analogous the files stored within that folder.
- This requires the BootstrapServerString and the Plaintext Apache Zookeeper connection string from MSK management console. 
- Three topics are created: 0a54b96ac143_pin, 0a54b96ac143_geo, and 0a54b96ac143_user. 

### Setting up MSK connect to connect external data to S3 bucket
- A feature of AWS MSK, enabling users to stream data to and from their MSK-hosted Apache kafka clusters. Specifically in moving data between data stores like S3 and external databases/file systems
- A Sink connector is created to send data from MSK cluster to a S3 bucket. This requires a MSK cluster, S3 bucket, IAM role and VPC (virtual private cloud) endpoint. The last enables data from cluster VPC and connector to be sent to destination.
- A plugin contains the logic of the connector. After downloading Confluent, a custom plugin is created within AWS which allows the connector to be created.  
- This will allow data to be sent from MSK cluster to S3 bucket in a newly created folder called topics. 

### Building a Kafka REST proxy integration method for the API
- REST APIs are standard for client-server communication. This provides a RESTful interface to a kafka cluster for simple produce and consume of messages.
- A HTTP method is used to integrate API with an endpoint on the backend. 
- Proxy integrations provide selected integration access to many resources and features at once, without specifying multiple resource paths using greedy parameter. 
- Invoke URL given aftern deploying the API. 
- Configure the REST proxt to communicate with desired MSK cluster and perform IAM authentication usiong the REST proxy package: confluent
- After deploying the API, you can use the requests package to invoke the url and send data to the S3 bucket.

### Using databricks to process data
- After setting up the infrastructure to batch stream data into the S3 bucket, Databrick's notebooks is used to analyse the data.
- The S3 bucket is mounted into Databricks and is then ready to be transformed . 
- Create a DAG file: Connects databricks cluster and executes a notebook (EDA). This can be done on the AWS MWAA

## Installation Instructions - Streaming 
### Set up Kinesis to stream data from the user, pin, and geo data
- create and configure a REST API with an Amazon Kinesis proxy integration.
- Create IAM role for permissions
- Configure API, creating resources and methods to enable the stream to POST data to the MWAA streams
- The above will create a new invoke url for the emulation python script to send data to

### Using Databricks to analyse and write to delta tables

## Usage instructions
- Managed Service Kafka - Used in conjunction with EC2 instance locally configured as Kafka cluster to create topics.
- MSK Connect - A feature of MSK to create a Sink connector plugin and send data from topics to S3 bucket
- S3 bucket for data storage. 
- API Gateway - Used to deploy an Proxy integration for REST APIs
- AWS Managed Workflow for Apache Airflow - Scheduled and monitored different tasks (workflows) to run the databricks analysis notebook. 
- AWS Kinesis - AWS Kinesis can collect streaming data such as event logs, social media feeds, application data, and IoT sensor data in real time or near real-time. Kinesis enables you to process and analyze this data as soon as it arrives, allowing you to respond instantly and gain timely analytics insights.

## File structure within SSH
- .pem file which is stored within the SSH client (WSL Ubuntu). This file enables user to connect to their EC2 instance. Found in Parameter store
- Java-1.8.0, Kafka_2.12-2.8.1, AWS MSK IAM authenticator. These are required to set up production to the cluster. 
- Confluent.io Amazon S3 Connector. This connector is a sink connecto that exports data from kafka topics to S3 objects in JSON (and other) format
- confluent-7.2.0 enables configuration of REST proxy to comms with MSK cluster. 
- user_posting_emulation_streaming.py. This file reads data using a DB engine connected to RDS and to send data the payload json format is equal to the format given in the MWAA when methods and resources were created.
- user_posting_emulation.py. Similar as above but it is done via batch processing which is POSTed. 

## File structure on Github
- user_posting_emulation.py: To emulate user's posts, a random time is used to extract a row of data from a RDS in AWS. The file consists of the class AWSDBConnector and functions to ingest and format the data into JSON format. 
- user_posting_emulation_streaming.py: A modified version of the above file where the invoke url is different. Instead the data is 'put' into MWAA's data streams.
- Pinterest-pipeline: This python file contains the CleanData class used to transform the Pinterest data and prepares it for S3 storage
- Streaming_Pinterest_Data.ipynb: This file reads data from Kinesis's data stream and also contains the CleanData class used to prepare data to be written to Delta lakes on Databricks

## License Information
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.