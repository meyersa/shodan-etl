import unittest
import logging 
import sys 

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from tests.shodanAPI import TestShodanAPIClass

if __name__ == '__main__': 
    unittest.main() 
