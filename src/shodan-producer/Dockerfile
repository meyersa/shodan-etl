FROM ubuntu:latest

# Upgrade
RUN apt update && apt upgrade -y 

# Install Python 
RUN apt install python3 

# Import producer code 
COPY ./src/shodan-producer . 

# Install Pip packages
RUN pip3 install -r requirements.txt 

RUN entrypoint.sh