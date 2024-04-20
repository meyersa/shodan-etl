# Enriches IP Information with Crowdsec
# TODO: Read data
# TODO: Interface with Crowdsec LAPI
# TODO: Subscribe to Kafka Producer
# TODO: Push data

from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time
import json 
import requests

def main():

    print("Gathering ENVs")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")
    crowdsec_lapi_url = get_env_variable("CROWDSEC_LAPI_URL")
    crowdsec_lapi_key = get_env_variable("CROWDSEC_LAPI_KEY")
    maxmind_api_url = get_env_variable("MAXMIND_API_URL")

    # Preparing headers for request
    crowdsec_header = {'X-Api-Key' : crowdsec_lapi_key}

    print("Connecting to Kafka")
    Consumer = KafkaConnection(kafka_connection, 'transformed')
    print("Starting loop")
    while True: 
        print("Polling")
        msg = Consumer.poll_message()

        if msg is None: 
            continue
        
        print("original msg", msg)
        msg.replace("'", "\"")
        msg = json.loads(msg)
        print("post msg", msg)

        for res in msg: 

            ip = res.get("ip")
            print("IP: ", ip)

            try: 
                maxmind_enrich = requests.get(f'{maxmind_api_url}{ip}').json()
            except: 
                print("Failed to query maxmind API")

            if maxmind_enrich:
                # res.update(maxmind_enrich)
                print("Maxmind Result:", maxmind_enrich)
            try:
                crowdsec_enrich = requests.get(f'{crowdsec_lapi_url}v1/decisions?ip={ip}', headers=crowdsec_header).json()
            except:
                print("Failed to query Crowdsec API")

            if crowdsec_enrich:
                # res.update(crowdsec_enrich)
                print("Crowdsec Result:", crowdsec_enrich)
            print(ip)

        print(msg) 
        time.sleep(5)


        

# Only run in main
if __name__ == "__main__":
    main()
