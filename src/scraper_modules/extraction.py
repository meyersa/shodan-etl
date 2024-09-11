import logging 

from scraper_modules.extraction_modules.shodanAPI import shodanAPI

class Extraction(): 
    def __init__(self, SHODAN_API_KEY, query) -> None:
        self.shodan = shodanAPI(SHODAN_API_KEY)
        self.query = query 

    def get(self) -> list: 
        """
        Get all extracted information
        """
        return self.shodan.raw_query(self.query)
        
