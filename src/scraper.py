"""
scraper.py 

Performs an ETL pipeline on incoming data from Shodan 

Extraction: 
- Uses Shodan's API to load the Data 

Transformation: 
- Drops unnecessary information from Shodan
- Uses Crowdsec to add ban information 
- Uses Maxmind to add geo information 

Load: 
- Saves to API to be stored
"""

import os
import logging 
import time 

from scraper_modules.extraction import Extraction
from scraper_modules.transformation import Transformation

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
# SHODAN_QUERY = os.getenv("SHODAN_QUERY")
SHODAN_QUERY = "ip:1.1.1.2"

CROWDSEC_LAPI_KEY = os.getenv("CROWDSEC_LAPI_KEY")
CROWDSEC_LAPI_URL = os.getenv("CROWDSEC_LAPI_URL")

# MAXMIND_API_URL = os.getenv("MAXMIND_API_URL")
MAXMIND_API_URL = "http://localhost:8080/"

SLEEP = os.getenv("SLEEP")

# Default 300 seconds 
if not SLEEP: 
    SLEEP = 300 

def main(): 
    """
    Calls other components 
    """
    logging.info('Starting ETL Cycle')

    logging.info('Checking ENV variables')
    if None in [SHODAN_API_KEY, CROWDSEC_LAPI_KEY, CROWDSEC_LAPI_URL]: 
        raise ValueError("Null ENV variables provided")

    logging.info('Passed ENV validation')

    logging.info('Initializing modules')
    eStage = Extraction(SHODAN_API_KEY, SHODAN_QUERY)
    tStage = Transformation(crowdsec_api_key=CROWDSEC_LAPI_KEY, crowdsec_api_url=CROWDSEC_LAPI_URL, maxmind_api_url=MAXMIND_API_URL)
    logging.info('Initialized modules')

    logging.info('Starting scraping loop')
    while True: 
        iter_res_st1 = eStage.get() 
        iter_res_st2 = tStage.get(iter_res_st1)


        logging.info(f'Sleeping for {SLEEP}s')
        time.sleep(SLEEP)        

if __name__ == "__main__": 
    main()
