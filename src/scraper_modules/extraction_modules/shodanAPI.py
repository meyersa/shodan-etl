import shodan
import logging 

class shodanAPI:
    """
    Shodan API Class 

    Connection class for interacting with the Shodan API.
    Wraps some methods and makes querying Shodan more reproducable 

    Args:
        api_key (str): The API key for accessing the Shodan service.
    """

    def __init__(self, api_key) -> None:
        """
        Initializes a new instance of the ShodanAPI class.

        Args:
            api_key (str): The API key for accessing the Shodan service.
        """
        logging.debug('Initializing Shodan class')

        self.api_key = api_key
        self.__connectToShodan()

    def __connectToShodan(self) -> None:
        """
        Connects to the Shodan API using the provided API key.
        """
        logging.debug('Connecting to shodan')

        self.api = shodan.Shodan(self.api_key)

        logging.debug('Connected to Shodan')

    def raw_count(self, query) -> int:
        """
        Perform a Shodan API query and returns the count of results 

        Args: 
            query: str to query against Shodan 

        Returns: 
            int: Number of items returned 

        Raises:
            ValueError: No Query passed through

        """
        logging.debug(f'Querying Shodan for count of "{query}"')

        if query is None:
            raise ValueError("Query is undefined")

        res = self.api.count(query) # type: dict

        resTotal = res.get("total")

        logging.debug(f'Found {resTotal} results from Shodan')

        return resTotal

    def raw_query(self, query) -> str:
        """
        Perform a Shodan API query. 

        Args: 
            query: str The query to search for. 

        Returns: 
            str: Result of query 

        Raises:
            ValueError: No query passed through
        """
        logging.debug(f'Querying Shodan for query "{query}"')

        if not query:
            raise ValueError("Query is undefined")

        result = self.api.search(query) # type: dict
        
        all_results = result.get("matches") # type: list
        num_results = result.get("total") # type: int

        logging.debug(f'Found {num_results} results from Shodan')
        
        if num_results <= 100:
            logging.debug(f'Found less than 100 results, so returning')
            return all_results

        logging.debug(f'Found more than 100 results, querying additional pages')

        page_num = 2
        while (page_num - 1) * 100 < num_results:
            cur_res = self.api.search(query, page=page_num) # type: dict

            all_results.append(cur_res.get("matches"))
            page_num += 1
                
        logging.debug(f'Returning matches')

        return all_results
