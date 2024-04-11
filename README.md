# Overview

Project that takes in batch/stream input from Shodan.io's API and feeds it into an ETL pipeline utilizing Apache Spark and Apache Kafka. 

ETL can be broken down into three major stages: extraction, transformation, and loading. 

## Extraction 

Taking in the actual data 

The plan is to use a Python program running in Docker that continually finds the right information and inputs it into a Kafka topic

### Shodan Producer Container 

- Function that queries Shodan API for the desired information
- Function that establishes the connection to the Kafka topic
- Function that uploads data to the established topic
- Function that handles the calls on a timer

- Dockerfile that wraps the code and installs the Python runtime
- Needs entrypoint.sh that starts this 


## Transformation 

In order to standardize this data, drop unnecessary information, and more, Apache Airflow will be utilized. 

> If this fails, the transformation will be done by the extraction step in order to preserve the "stream" aspect of the project

### Airflow Transformation Container

- Converts datatypes if needed 
- Drops repetive information 
- Drops null values 
- Drops outliers
- Drops unneeded information

- Either in prebuilt Docker container or Dockerfile defined to install this 

### Crowdsec Enrich Data 

- Crowdsec LAPI Container
- Python container that queries LAPI with IPs for their status

## Loading 

To get the data back to consumers the final data will be put into a Kafka topic that can easily be subscribed to 

### MongoDB Connector

- Store consumed data in MongoDB for historic trends

### Python Flask API 

- Connects to Kafka topic 
- Converts to stats about incoming topic
- Exposes API for the stats 

- Dockerfile that wraps the code and installs the Python runtime
- Needs entrypoint.sh that starts this 

### Python Dispatcher

- Connects to Kafka topic 
- Interprets the data for matching hostnames/IPs of CMICH
- Sends alert to Discord if found 

- Dockerfile that wraps the code and installs the Python runtime
- Needs entrypoint.sh that starts this 

### Python Flask Display 

- Displays the stats from the Flask API 
- Displays an iFrame of the discord alert channel to show alerts

- Dockerfile that wraps the code and installs the Python runtime
- Needs entrypoint.sh that starts this 

## Kafka 

- Connects the pipeline stages together 
- Ensures delivery of data
- Easy connection point for feeding data to multiple sources 

## Meta 

- Docker compose that wraps the build information into one for convenient deployment
- This can be easily converted to charts for K8