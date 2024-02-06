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

# endpoint url
http://ec2-34-235-131-58.compute-1.amazonaws.com:8082/{proxy}

# Connect EC2 to S3. then create plugin
- A plugin will contain the code that defines the logic of our connector. This requires downloading Confluent.io Amazon S3 connector. This connector is a sink connector that exports data from kafka topics to S3 objects in either JSON, Avro or Bytes format
- In the EC2 instance, download the above within a folder called kafka-connect-s3. Copy the connector to the S3 bucket 
- aws s3 cp ./confluentinc-kafka-connect-s3-10.0.3.zip s3://<BUCKET_NAME>/kafka-connect-s3/ - After runnning this code, you should see it in the S3 AWS.
- Within MSK Connector, create custom plugin and select the ZIP file within the S3 bucket as the S3 url. 

# Create connector
- Within MSK Connect, create connector. Select plugin created from above and configure the settings. topics.regex == user-id, s3.bucket.name = bucket.  selecting the EC2-iam-ec2-access
- After creating both plugin and connector, should be able to send data from MSK to S3.

# Create REST proxy API
Enables easier consuming and production of messages, view state of cluster, perform adminstrative tasks without using native kafka protocals or clients

# invoke api url
https://c9joj9e3ij.execute-api.us-east-1.amazonaws.com/test/topics/0a54b96ac143.pin

# topic names 
0a54b96ac143.pin
0a54b96ac143.geo
0a54b96ac143.user

# Starting REST proxy within the confluent bin folder
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties

# Git
Create git repository on github and copy url
git init
git remote add origin (url)


