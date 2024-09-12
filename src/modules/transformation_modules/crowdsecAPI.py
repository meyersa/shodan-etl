import logging
import requests
import json 


class crowdsecAPI:
    """
    Crowdsec API Class 

    Connection class for interacting with the Crowdsec LAPI
    Wraps some methods and makes querying the LAPI easier 
    """

    def __init__(self, crowdsec_api_key, crowdsec_api_url) -> None:
        """
        Initializes a new instance of the crowdsecLAPI class

        Args:
            crowdsec_lapi_key (str): The API key for accessing the Crowdsec LAPI
            crowdsec_lapi_url (str): The URL of the Crowdsec LAPI
        """
        logging.debug('Initializing Crowdsec class')

        if None in [crowdsec_api_key, crowdsec_api_url]: 
            raise ValueError("Cannot have null inputs")

        self.crowdsec_api_key = crowdsec_api_key
        self.crowdsec_api_url = crowdsec_api_url 

        logging.debug('Initialized Crowdsec class')

    def query(self, ip: str) -> dict:
        """
        Query the Crowdsec LAPI 

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
        logging.debug(f'Querying Crowdsec LAPI for {ip}')

        res = None
        try: 
            res = requests.get(f'{self.crowdsec_api_url}v1/decisions?ip={ip}',
                               headers={"X-Api-Key": self.crowdsec_api_key})
            
            if res is None: 
                raise ValueError('Received nothing back')

            if res.status_code != 200: 
                raise ValueError(f'Non 200 status {res.status_code}')

        except Exception as e: 
            logging.exception('Unable to query Crowdsec')
            return 
        
        logging.debug(f'Queried Crowdsec API, processing')

        crowdsec_res = json.loads(res.content) 

        if crowdsec_res is None: 
            logging.debug(f'Returning, found no bans')
            return {'is_banned': False}

        logging.debug(f'Found {len(crowdsec_res)} bans')

        returnables = dict()
        returnables['is_banned'] = True 
        returnables['bans'] = dict() 

        for ban in crowdsec_res: 
            ban = ban # type: dict

            cur_ban = dict() 
            cur_id = ban.get("id")

            cur_ban["duration"] = ban.get("duration")
            cur_ban["origin"] = ban.get("origin")
            cur_ban["scenario"] = ban.get("scenario")

            returnables['bans'][cur_id] = cur_ban

        logging.debug(f'Returning dict with ban information')

        return returnables