# Overview

Project that takes in batch/stream input from Shodan.io's API and feeds it into an ETL pipeline utilizing Apache Flume, Apache Spark, and Apache Kafka. 

ETL can be broken down into three major stages: extraction, transformation, and loading. 

### Extraction 

Taking in the actual data 

The plan is to use Apache Flume as an extraction tool to interact with the Shodan API. 

>If this fails, either a Python or NodeJS program will take care of that and feed it into a raw Kafka topic. 

### Transformation 

In order to standardize this data, drop unnecessary information, and more, Apache Airflow will be utilized. 

> If this fails, the transformation will be done by the extraction step in order to preserve the "stream" aspect of the project

### Loading 

To get the data back to consumers the final data will be put into a Kafka topic that can easily be subscribed to 


### Displaying 

If there's extra time, a flask dashboard will be built to display the Shodan data and statistics about the pipeline