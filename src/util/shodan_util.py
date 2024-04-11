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
            str: Error message if an API error occurs.
        """
        try:
            return self.api.search(f"asn:{asn}")

        except shodan.APIError as e:
            return f"Error: {e}"
