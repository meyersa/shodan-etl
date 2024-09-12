import logging
import requests
import json 


class maxmindAPI:
    """
    MaxMind API Class 

    Connection class for interacting with the MaxMind LAPI
    Wraps some methods and makes querying the LAPI easier 
    """

    def __init__(self, maxmind_api_url) -> None:
        """
        Initializes a new instance of the maxmindAPI class

        Args:
            maxmind_api_url (str): The URL for accessing the MaxMind API
        """
        logging.debug('Initializing MaxMind class')

        if maxmind_api_url is None:
            raise ValueError("Cannot have null inputs")

        self.maxmind_api_url = maxmind_api_url

        logging.debug('Initialized MaxMind class')

    def query(self, ip: str) -> dict:
        """
        Query the MaxMind LAPI 

        Inputs: 
            ip: str 

        Returns: 
            dict: {
                'is_banned': if banned
                'ban_<id>': {
                    'duration': of ban 
                    'origin': of ban 
                    'scenario': of ban
                }
            }
        """
        logging.debug(f'Querying MaxMind API for {ip}')

        res = None
        try: 
            res = requests.get(f'{self.maxmind_api_url}{ip}')
            
            if res is None: 
                raise ValueError('Received nothing back')

            if res.status_code != 200: 
                raise ValueError(f'Non 200 status {res.status_code}')

        except Exception as e: 
            logging.exception('Unable to query MaxMind API')
            return 
        
        logging.debug(f'Queried MaxMind API, processing')

        maxmind_res = json.loads(res.content) # type: dict 

        # Unneeded
        del maxmind_res["asn"]
        del maxmind_res["asnOrganization"]
        del maxmind_res["asnNetwork"]

        logging.debug('Returning MaxMind info')

        # To merge later
        returnables = dict() 
        returnables["maxmind"] = maxmind_res

        return returnables