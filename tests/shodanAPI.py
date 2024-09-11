import unittest
import os 

from src.scraper_modules.extraction_modules.shodanAPI import shodanAPI

class TestShodanAPIClass(unittest.TestCase):

    def setUp(self) -> None:
       self.shodan = shodanAPI(os.getenv("SHODAN_API_KEY"))

    def test_class(self) -> None: 
        self.assertIsNotNone(self.shodan) 

    def test_query_count(self) -> None: 
        self.assertGreater(self.shodan.raw_count("ip:1.1.1.1"), 0)

    def test_query(self) -> None: 
        self.assertGreater(len(self.shodan.raw_query('ip:1.1.1.1')), 0)