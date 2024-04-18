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

    @staticmethod
    def trim_results(results):
        """
        Trim the results returned by the Shodan API to remove excessively large entries.

        Args:
            results (list): List of results returned by the Shodan API.

        Returns:
            list: Trimmed list of results.
        """
        if results is None or len(results) == 0:
            raise ValueError("No result input")

        trimmed_results = []
        for host in results:
            trimmed_host = {}
            for key, value in host.items():
                if isinstance(value, dict):
                    continue  # Skip dictionary results
                elif isinstance(value, str) and len(value) > 256:
                    continue  # Skip string results over 256 characters
                elif isinstance(value, str):
                    trimmed_host[key] = value
                elif isinstance(value, int):
                    trimmed_host[key] = str(value)
            if trimmed_host:
                trimmed_results.append(trimmed_host)

        if not trimmed_results:
            raise ValueError("Removed all elements")
        
        return trimmed_results

    def raw_count(self, query):
        """
        Perform a Shodan API count by ASN (Autonomous System Number). 

        Args: 
            asn (str): The ASN to search for. 

        Returns: 
            int: Number of items returned 

        Raises:
            ValueError: No ASN passed through
        """
        if query is None:
            raise ValueError("Query is undefined")

        return int(self.api.count(query))

    def raw_query(self, query):
        """
        Perform a Shodan API query. 

        Args: 
            query (str): The query to search for. 

        Returns: 
            str: Result of query 

        Raises:
            ValueError: No query passed through
        """
        if not query:
            raise ValueError("Query is undefined")

        result = self.api.search(query)
        num_results = result['total']
        all_results = self.trim_results(result['matches'])

        if num_results <= 100:
            return all_results

        page_num = 2
        while (page_num - 1) * 100 < num_results:
            cur_res = self.api.search(query, page=page_num)
            all_results.extend(self.trim_results(cur_res['matches']))
            page_num += 1
                
        print(f'Initial: {num_results} | Post: {len(all_results)}')
        
        json_result = json.dumps(all_results)
        return all_results
