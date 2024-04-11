import shodan

class shodanAPI:
    """
    Connection class for interacting with the Shodan API.

    Args:
        api_key (str): The API key for accessing the Shodan service.
    """

    def __init__(self, api_key):
        """
        Initializes a new instance of the ShodanAPI class.

        Args:
            api_key (str): The API key for accessing the Shodan service.
        """
        self.api_key = api_key
        self.__connectToShodan()

    def __connectToShodan(self):
        """
        Connects to the Shodan API using the provided API key.
        """
        self.api = shodan.Shodan(self.api_key)

    def lookup_by_asn(self, asn):
        """
        Perform a Shodan API lookup by ASN (Autonomous System Number).

        Args:
            asn (str): The ASN to search for.

        Returns:
            dict: A dictionary containing the search results.

        Raises:
            ValueError: No ASN passed through
        """
        if asn is None:
            raise ValueError("ASN is undefined")
        
        return self.api.search(f"asn:{asn}")
        
    def count_by_asn(self, asn): 
        """
        Perform a Shodan API count by ASN (Autonomous System Number). 
        
        Args: 
            asn (str): The ASN to search for. 
            
        Returns: 
            int: Number of items returned 
            
        Raises:
            ValueError: No ASN passed through
        """
        if asn is None: 
            raise ValueError("ASN is undefined")
        
        return int(self.api.count(f"asn:{asn}").get('total'))
    