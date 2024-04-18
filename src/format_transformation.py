# Subscribe to Kafka 
# Watch for new entries
# Standardize data
# Send to processed topic

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
    while True: 
        time.sleep(5)

        print("Polling")
        msg = Consumer.poll_message()

        if msg is None: 
            continue

        print(msg) 

        with open('output.txt', 'w') as f: 
            for entry in msg:
                f.write(entry)

    with open('./src/output.txt') as msg_file:
        msg_file = msg_file.read()

        for key, value in msg_file: 
            print(key + " " + value)
        
        
        # msg_file = msg_file.replace("'", "\"")
        
        # msg_json = json.dumps(msg_file.read(), separators=(',', ':'), indent=4)
        msg_json = json.loads(msg_file)
        print(msg_json)
        

# Only run in main
if __name__ == "__main__":
    main()
