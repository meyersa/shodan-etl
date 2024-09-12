
import time
from pymongo import MongoClient
import logging


class mongoLoad():
    def __init__(self, mongo_url, mongo_db) -> None:
        logging.debug('Initializing Mongo Load class')

        if None in [mongo_url, mongo_db]:
            raise ValueError("Invalid MongoLoad values provided")

        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

        self.initMongo()

        logging.debug('Initialized Mongo Load class')

    def initMongo(self) -> None:
        logging.debug('Starting Mongo Client')

        self.mongo = MongoClient(self.mongo_url)[self.mongo_db]
        self.ip_col = self.mongo['ips']

        logging.debug('Started Mongo Client')

    def get(self, inp_ip) -> list[dict]: 
        logging.debug('Getting all documents from collection')
        return self.ip_col.find_one({"ip_str": inp_ip})

    def post(self, inp: dict) -> bool: 
        logging.debug('Uploading document to collection')

        inp_ip = inp.get("ip_str")

        if self.ip_col.find_one({"ip_str": inp_ip}): 
            logging.warning("Entry already existed in collection, something went wrong")
            return False
        
        return bool(self.ip_col.insert_one(inp))