# Shodan Producer Main.py
#
# Handler for the Shodan Producer container
# - Loads the environment variables
#   - Handles .env location
#   - Handles missing environment variables
# - Connects to Shodan API
# - Runs specified Queries
# TODO:  - Loads the queries
# TODO:  - Handles failures of queries
# TODO:- Dispatches the results to Kafka topic
# TODO:- Continually runs on a specified interval

from lib.shodan_util import shodanAPI
from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable

def main():
    shodan_api_key = get_env_variable("SHODAN_API_KEY")
    asn = get_env_variable("ASN")

    api = shodanAPI(shodan_api_key)
    producer = KafkaConnection('localhost:29092', 'shodan-asn-count')

    producer.send(value=api.count_by_asn(asn))

# Only run in main
if __name__ == "__main__":
    main()
