FROM ubuntu:latest

# Upgrade
RUN apt update && apt upgrade -y 

# Install Python 
RUN apt install -y python3 python3-pip

# Import producer code 
COPY ./src /src

# Import requirements 
COPY ./requirements.txt /requirements.txt

# Install Pip packages
RUN pip3 install -r /requirements.txt 

# Copy entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]