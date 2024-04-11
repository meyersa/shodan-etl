# TODO: Wrapper that calls kafka producer connection, shodan api, and kafka producer
# Should verify data was received 
# Should constantly verify connection or retry

from dotenv import load_dotenv
from pathlib import Path 
import os
from ..util.shodan_util import shodanAPI

def main(): 
    print(os.getcwd())
    # Load local .env for prod
    if os.path.exists('.env'):
        load_dotenv()

    # Load root .env if dev
    elif os.path.exists('../../.env'): 
        load_dotenv('../../.env')

    # Exit if neither
    else: 
        raise FileNotFoundError("Neither local .env nor fallback .env file found")
    
    shodan_api_key = os.getenv('SHODAN_API_KEY')
    asn = os.getenv('ASN')

    if not (shodan_api_key and asn): 
        raise RuntimeError("Missing environment variable")
    
    api = shodanAPI(shodan_api_key)
    print(api.lookup_by_asn(asn))

 

# Only run in main
if __name__ == "__main__": 
    main()