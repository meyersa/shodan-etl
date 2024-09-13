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
import sys 

from modules.extraction import Extraction
from modules.transformation import Transformation
from modules.load import Load

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
# SHODAN_QUERY = os.getenv("SHODAN_QUERY")
SHODAN_QUERY = "ASN:AS27274"

CROWDSEC_LAPI_KEY = os.getenv("CROWDSEC_LAPI_KEY")
CROWDSEC_LAPI_URL = os.getenv("CROWDSEC_LAPI_URL")

# MAXMIND_API_URL = os.getenv("MAXMIND_API_URL")
MAXMIND_API_URL = "http://localhost:8080/"

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

# Between runs
SLEEP = os.getenv("SLEEP")
if not SLEEP: 
    SLEEP = 1 * 60 * 60 * 24 * 7 

# Between batch processing
SHORT_SLEEP = os.getenv("SHORT_SLEEP")
if not SHORT_SLEEP:
    SHORT_SLEEP = 60

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
    global eStage
    eStage = Extraction(SHODAN_API_KEY, SHODAN_QUERY)

    global tStage
    tStage = Transformation(crowdsec_api_key=CROWDSEC_LAPI_KEY, crowdsec_api_url=CROWDSEC_LAPI_URL, maxmind_api_url=MAXMIND_API_URL)
    
    global lStage
    lStage = Load(MONGO_URL, MONGO_DB) 
    logging.info('Initialized modules')

    while True: 
        iter_res_st1 = eStage.get() 

        batchProcess(iter_res_st1) 

        logging.info(f'Sleeping for {SLEEP}s')
        time.sleep(SLEEP)        

def batchProcess(inp: list) -> None: 
    start = 0 
    batchSize = 10

    while True: 
        logging.info(f'Processing batch {start / batchSize} out of {len(inp) / batchSize}')

        cur_batch = inp[start:start + batchSize]

        res_st2 = tStage.get(cur_batch)
        res_st3 = lStage.post(res_st2)

        logging.info(f'Processed batch {len(inp) / batchSize}')

        start += batchSize 

        if start > len(inp): 
            break 

        logging.info(f'Sleeping for {SHORT_SLEEP}s')
        time.sleep(SHORT_SLEEP)

    logging.info(f'Finished batch')

if __name__ == "__main__": 
    main()
