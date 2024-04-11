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

from dotenv import load_dotenv
import os
from lib.shodan_util import shodanAPI
from lib.kafka_util import KafkaConnection

def main():
    # Load local .env for prod
    if os.path.exists(".env"):
        load_dotenv()

    # Load root .env if dev
    elif os.path.exists("../../.env"):
        load_dotenv("../../.env")

    # Exit if neither
    else:
        raise FileNotFoundError("Neither local .env nor fallback .env file found")

    shodan_api_key = os.getenv("SHODAN_API_KEY")
    asn = os.getenv("ASN")

    if not (shodan_api_key and asn):
        raise RuntimeError("Missing environment variable")

    api = shodanAPI(shodan_api_key)
    producer = KafkaConnection('localhost:29092', 'shodan-asn-count')

    print(api.lookup_by_asn(asn))
    producer.send(value=api.count_by_asn(asn))

# Only run in main
if __name__ == "__main__":
    main()
