# Enriches IP Information with Crowdsec
# TODO: Read data
# TODO: Interface with Crowdsec LAPI
# TODO: Subscribe to Kafka Producer
# TODO: Push data

from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time
import requests
import json


def main():

    print("Gathering ENVs")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")
    crowdsec_lapi_url = get_env_variable("CROWDSEC_LAPI_URL")
    crowdsec_lapi_key = get_env_variable("CROWDSEC_LAPI_KEY")
    maxmind_api_url = get_env_variable("MAXMIND_API_URL")

    # Preparing headers for request
    crowdsec_header = {"X-Api-Key": crowdsec_lapi_key}

    # Start delay
    delay = int(get_env_variable("DELAY"))
    time.sleep(delay)

    print("Connecting to Kafka")
    Consumer = KafkaConnection(kafka_connection, "transformed")
    Producer = KafkaConnection(kafka_connection, "enriched")
    print("Starting loop")

    while True:
        msg = Consumer.poll_message()

        # Skip if no result
        if msg is None:
            continue

        # Get the IP
        ip = msg.get("ip_str")
        msg: dict

        """
        Query MaxMind DB for location information

        Appends the following: 
        - country
        - stateprov
        - stateprovCode
        - city
        - latitude
        - longitude
        - continent
        - timezone
        - *more depending on location such as usMetroCode

        Does not preserve from Maxmind
        - asn
        - asnOrganization
        - asnNetwork
        """
        maxmind_enrich = None
        try:
            maxmind_enrich = requests.get(f"{maxmind_api_url}{ip}")
            if maxmind_enrich is None:
                raise ValueError

        except:
            print("Failed to query maxmind API")

        if maxmind_enrich.status_code == 200:
            maxmind_res = json.loads(maxmind_enrich.content)

            del maxmind_res["asn"]
            del maxmind_res["asnOrganization"]
            del maxmind_res["asnNetwork"]

            # Merge into result
            msg.update(maxmind_res)

        """
        Query Crowdsec (Local) for location information

        Appends the following: 
        - is_banned (depends on result)
        - bans
            - duration
            - id
            - origin
            - scenario

        Does not preserve from Crowdsec
        - scope
        - type
        - value
        """
        crowdsec_enrich = None
        try:
            crowdsec_enrich = requests.get(
                f"{crowdsec_lapi_url}v1/decisions?ip={ip}", headers=crowdsec_header
            )
            if crowdsec_enrich is None:
                raise ValueError
        except:
            print("Failed to query Crowdsec API")

        if crowdsec_enrich.status_code == 200 and crowdsec_enrich.content != b"null":
            for ban in json.loads(crowdsec_enrich.content):
                ban: dict
                cur_ban = dict()
                ban_id = ban.get("id")

                cur_ban["duration"] = ban.get("duration")
                cur_ban["id"] = ban.get("id")
                cur_ban["origin"] = ban.get("origin")
                cur_ban["scenario"] = ban.get("scenario")

                msg[f"ban_{ban_id}"] = cur_ban

        try:
            Producer.send(value=msg, key=ip)

        except ValueError:
            print("Failed to send: ran into an error transforming data")


# Only run in main
if __name__ == "__main__":
    main()
