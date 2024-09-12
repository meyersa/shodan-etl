"""
Class to transform incoming data 

"""
from modules.transformation_modules.clean import clean_dict
from modules.transformation_modules.crowdsecAPI import crowdsecAPI
from modules.transformation_modules.mindmaxAPI import maxmindAPI
from modules.transformation_modules.flatten import flatten_loc
from modules.transformation_modules.merge import merge_dict

import time


class Transformation():
    def __init__(self, crowdsec_api_key, crowdsec_api_url, maxmind_api_url) -> None:
        self.crowdsecAPI = crowdsecAPI(
            crowdsec_api_key=crowdsec_api_key, crowdsec_api_url=crowdsec_api_url)
        self.mindmaxAPI = maxmindAPI(maxmind_api_url)

    def get(self, inp: list[dict]) -> list[dict]:
        clean_inp = list()

        for inp_dict in inp:
            inp_dict = clean_dict(inp_dict)

        inp = merge_dict(inp)

        for inp_dict in inp:
            ip = inp_dict.get("ip_str")

            inp_dict.update(self.crowdsecAPI.query(ip))
            inp_dict.update(self.mindmaxAPI.query(ip))

            inp_dict = flatten_loc(inp_dict)
            inp_dict = clean_dict(inp_dict)

            clean_inp.append(inp_dict)

            # Don't want to stress anything too hard
            time.sleep(1)

        return clean_inp
