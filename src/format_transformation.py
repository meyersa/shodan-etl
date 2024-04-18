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
        print("Polling")
        results = Consumer.poll_message()

        if results is None: 
            continue
            
        results = json.loads(results)

        with open('output.txt', 'w') as f: 
            for host in results: 
                # f.write(host)
                print("Object: ", host)                                    

        time.sleep(5)

# Only run in main
if __name__ == "__main__":
    main()
