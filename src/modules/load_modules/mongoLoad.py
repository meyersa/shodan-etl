
from pymongo import MongoClient
import logging


class mongoLoad():
    """
    Mongo load module 
    Wraps the MongoDB operations into a class for easier reuse 
    """

    def __init__(self, mongo_url, mongo_db) -> None:
        """
        Init a Mongo Load class 
        
        Inputs: 
            mongo_url: str for Mongo to connect to 
            mongo_db: str for Mongo to connect to 
        """
        logging.debug('Initializing Mongo Load class')

        if None in [mongo_url, mongo_db]:
            raise ValueError("Invalid MongoLoad values provided")

        self._mongo_url = mongo_url
        self._mongo_db = mongo_db

        self.initMongo()

        logging.debug('Initialized Mongo Load class')

    def initMongo(self) -> None:
        """
        Mongo Init 
        
        Connect to Mongo client and then save it locally for use 
        Also connect to collection and save that 
        """
        logging.debug('Starting Mongo Client')

        self.mongo = MongoClient(self._mongo_url)[self._mongo_db]
        self.ip_col = self.mongo['ips']

        logging.debug('Started Mongo Client')

    def get(self, inp_ip) -> dict:
        """
        Get method 
        
        Gets specified input IP from collection 

        Inputs: 
            inp_ip: str to get from MongoDB collection 

        Returns: 
            dict: document that is returned
        """
        logging.debug(f'Getting IP {inp_ip} from collection')
        return self.ip_col.find_one({"ip_str": inp_ip})

    def post(self, inp: dict) -> bool:
        """
        Post method 
        
        Puts a Mongo document into collection 
        
        Inputs: 
            inp_ip: dict to insert
            
        Returns: 
            bool: status of post
        """
        logging.debug('Uploading document to collection')

        inp_ip = inp.get("ip_str")

        dup_check = self.ip_col.find_one({"ip_str": inp_ip})

        # Nothing found
        if not dup_check: 
            return bool(self.ip_col.insert_one(inp))

        dup_check = dup_check # type: dict 
        dup_check.pop("_id")
        
        # Check if they are the same 
        if dup_check == inp: 
            return True 
        
        # Not the same
        logging.debug('Found a duplicate, replacing it')
        return self.replace(inp)

    def replace(self, inp: dict) -> bool: 
        """
        Replace method 
        Takes in an input dict and replaces the existing document
        
        Inputs: 
            inp: dict to replace 
            
        Returns: 
            bool: if it was successful
        """
        logging.debug('Updating document in collection')

        inp_ip = inp.get("ip_str")
        old_inp = self.get(inp_ip)

        # Get the data fields, since these can change
        new_data = inp.get("data")
        old_data = old_inp.get("data") # type: dict

        # Update old with the new data if they are different
        if new_data != old_data:
            inp.get("data").update(old_data)

        # Reinsert the document
        return bool(self.ip_col.replace_one({"ip_str": inp_ip}, inp))
