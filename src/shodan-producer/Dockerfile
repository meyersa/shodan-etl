FROM ubuntu:latest

# Upgrade
RUN apt update && apt upgrade -y 

# Install Python 
RUN apt install python3 

# Import producer code 
COPY ./src/shodan-producer . 

RUN entrypoint.sh