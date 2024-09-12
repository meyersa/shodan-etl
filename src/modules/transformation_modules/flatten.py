"""
Helper function to merge in data after processing
"""

import logging 

def flatten_loc(inp: dict) -> dict: 
    """
    Combine the MaxMind and Shodan location information
    
    Favors MaxMind
    """
    logging.debug(f'Flattening location for {inp.get("ip_str")}')

    shod_loc = inp.get("location")
    mm_loc = inp.get("maxmind")

    del inp["location"] 

    # Just keep shodan info
    if mm_loc: 
        del mm_loc["timezone"]
        del mm_loc["accuracyRadius"]

        inp["location"] = mm_loc
        return inp 
    
    # Else make something with Shodan
    inp["location"] = {
        "country": shod_loc.get("country_code"),
        "latitude": shod_loc.get("latitude"),
        "longitude": shod_loc.get("longitude"),
        "continent": shod_loc.get("continent") 

    }

    return inp
