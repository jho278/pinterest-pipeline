# Emulation of the Pinterest data pipeline
For my final project with AICore, I will emulate the data pipeline for the Pinterest posts using a combination of AWS, Databricks and Python in VS Code. I aim to develop a workflow covering: 
- Data ingestion of the Pinterest data into AWS via Apache Kafka in an EC2 instance. 
- Data storage of the Pinterest data in a S3 object. 
- Mounting the S3 storage in Databricks for transformation and analysis. 

I will have demonstrated the application of my knowledge in AWS by processing data in real-time and creating a workflow to analyse the data to inform my stakeholders and provide analysis to support decision-making. 

# Installation Instructions
## EC2 instance
- Set up EC2 instance on client machine (within AWS) and configure to run MSK cluster (Apache Kafka client machine). 
- Within EC2 client machine, install 3 packages: Java-1.8.0, Kafka_2.12-2.8.1, AWS MSK IAM authenticator. The authenticator authorises users for production to the cluster. 
- Set the CLASSPATH environment variable in the ~/.bashrc to automate location of the JAR file (authenticator)
- Configure permissions in AWS IAM roles. This includes adding principal type in trust relationship, ensuring ARN matches with ec2-access-role
- You should now be able to connect to the EC2 instance and run Kafka. 

## Kafka topics
- This requires the BootstrapServerString and the Plaintext Apache Zookeeper connection string from MSK management console. 
- Three topics are created: 0a54b96ac143_pin, 0a54b96ac143_geo, and 0a54b96ac143_user. 

## Setting up MSK connect to connect external data to S3 bucket
- A feature of AWS MSK, enabling users to stream data to and from their MSK-hosted Apache kafka clusters. Specifically in moving data between data stores like S3 and external databases/file systems
- A Sink connector is created to send data from MSK cluster to a S3 bucket. This requires a MSK cluster, S3 bucket, IAM role and VPC (virtual private cloud) endpoint. The last enables data from cluster VPC and connector to be sent to destination.
- A plugin contains the logic of the connector. After downloading Confluent, a custom plugin is created within AWS which allows the connector to be created.  
- This will allow data to be sent from MSK cluster to S3 bucket in a newly created folder called topics. 

## Building a Kafka REST proxy integration method for the API
- REST APIs are standard for client-server communication. This provides a RESTful interface to a kafka cluster for simple produce and consume of messages.
- A HTTP method is used to integrate API with an endpoint on the backend. 
- Proxy integrations provide selected integration access to many resources and features at once, without specifying multiple resource paths using greedy parameter. 
- Invoke URL given aftern deploying the API. 
- Configure the REST proxt to communicate with desired MSK cluster and perform IAM authentication usiong the REST proxy package: confluent

# Usage instructions
- Managed Service Kafka - Used in conjunction with EC2 instance locally configured as Kafka cluster to create topics.
- MSK Connect - A feature of MSK to create a Sink connector plugin and send data from topics to S3 bucket
- S3 bucket for data storage. 
- API Gateway - Used to deploy an Proxy integration for REST APIs
- 

# File structure within SSH
- .pem file which is stored within the SSH client (WSL Ubuntu). This file enables user to connect to their EC2 instance. Found in Parameter store
- Java-1.8.0, Kafka_2.12-2.8.1, AWS MSK IAM authenticator. These are required to set up production to the cluster. 
- Confluent.io Amazon S3 Connector. This connector is a sink connecto that exports data from kafka topics to S3 objects in JSON (and other) format
- confluent-7.2.0 enables configuration of REST proxy to comms with MSK cluster. 

# License Information
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.