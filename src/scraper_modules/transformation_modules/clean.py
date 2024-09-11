"""
Helper Functions to trim results coming from Shodan

We only really need to keep: 
- asn 
- isp 
- hostnames
- domains
- location
- ip_str
- port 
- data 
- org 
"""

import logging 

def clean_dict(inp: dict) -> dict: 
    """
    Apply cleaning to the incoming dictionary
    """
    logging.debug(f'Cleaning input dictionary') 

    cln_dict_stg1 = sel_fields(inp) 
    cln_dict_stg2 = clean_fields(cln_dict_stg1)
    cln_dict_stg3 = drop_na(cln_dict_stg2)

    return cln_dict_stg3

def sel_fields(inp: dict) -> dict: 
    """
    Only retain useful fields: 
        - asn
        - os
        - timestamp
        - isp
        - hostnames
        - domains
        - location
        - ip_str
        - http
        - port 
        - data
        - org
        - is_banned
        - bans
    """
    keep_fields = ['asn', 'os', 'timestamp', 'isp', 'hostnames', 'location', 'domains', 'org', 'data', 'port', 'ip_str', 'http', 'is_banned', 'bans']
    new_dict = dict() 

    for k, v in inp.items(): 
        if k not in keep_fields: 
            continue

        new_dict[k] = v 

    return new_dict 

def clean_fields(inp: dict) -> dict: 
    """
    Function to clean incoming fields 
    
    - Strip whitespace 
    - Strings should be clipped at 256 char
    - Special characters should be removed 
    """
    for k, inpV in inp.items():
        try:
            inpV = str(inpV).strip()

            # Shorten
            if len(inpV) > 256: 
                inpV = inpV[:252] + "..."

            # Remove special char
            # TODO: See if necessary 
            
        except: 
            inpV = None

    return inp 
    
def drop_na(inp: dict) -> dict: 
    return {k: v for k, v in inp.items() if v is not None}
