# Enriches IP Information with Crowdsec
# TODO: Read data
# TODO: Interface with Crowdsec LAPI
# TODO: Subscribe to Kafka Producer
# TODO: Push data

from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time
import json 

def main():
    print("Gathering ENVs")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")
    
    print("Connecting to Kafka")
    Consumer = KafkaConnection(kafka_connection, 'shodan-producer')
    
    print("Starting loop")
    # while True: 
    #     time.sleep(5)

    #     print("Polling")
    #     msg = Consumer.poll_message()

    #     if msg is None: 
    #         continue

    #     print(msg) 

    #     with open('output.txt', 'w') as f: 
    #         for entry in msg:
    #             f.write(entry)

    with open('./src/output.txt') as msg_file:
        # Read the contents of the file
        json_string = msg_file.read()

        # Load the JSON string into a Python data structure
        data = json.loads(json_string)

        # Now you can work with the data
        print(data)
        

# Only run in main
if __name__ == "__main__":
    main()
