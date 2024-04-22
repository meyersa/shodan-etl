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
    Producer = KafkaConnection(kafka_connection, 'transformed')

    print("Starting loop")
    while True: 
        print("Polling")
        results = Consumer.poll_message()
        
        if results is None: 
            continue
        
        results = json.loads(results)
        num_results = 0
        
        # Make a list of each individual result and send to Kafka stream one by one
        for result in results: 
            num_results += 1

            try:
                Producer.send(value=result)                
            
            except ValueError: 
                print("Failed to send: ran into an error querying the Shodan API.. Continuing")
        
        print(f'Sent {num_results} parsed IPs')
        time.sleep(5)

# Only run in main
if __name__ == "__main__":
    main()
