# Enriches IP Information with Crowdsec
# TODO: Subscribe to Kafka Consumer
# TODO: Read data
# TODO: Interface with Crowdsec LAPI
# TODO: Subscribe to Kafka Producer
# TODO: Push data

from lib.shodan_util import shodanAPI
from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable

def main():
    shodan_api_key = get_env_variable("SHODAN_API_KEY")
    asn = get_env_variable("ASN")

    api = shodanAPI(shodan_api_key)
    Consumer = KafkaConnection('localhost:29092', 'shodan-asn-count')

    while True: 
        msg = Consumer.poll_message()

        if msg is None: 
            continue

        print(msg) 

        

# Only run in main
if __name__ == "__main__":
    main()
