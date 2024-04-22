FROM python:3

# Import requirements 
COPY ./requirements.txt /requirements.txt

# Install Pip packages
RUN pip install -r /requirements.txt 

COPY ./src /src 

WORKDIR /src