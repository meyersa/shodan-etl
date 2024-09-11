def merge_dict(inp: list) -> list:
    """
    Merge the incoming dictionary on IP addresses 

    Combines the Data by putting in dict with key as hash
    """
    returnables = dict()

    for inp_dict in inp:
        inp_dict = inp_dict  # type: dict

        cur_ip = inp_dict.get("ip_str")
        uniq_dict = {
            "asn": inp_dict.get("asn"),
            "isp": inp_dict.get("isp"),
            "hostnames": inp_dict.get("hostnames"),
            "location": inp_dict.get("location"),
            "ip": inp_dict.get("ip"),
            "domains": inp_dict.get("domains"),
            "org": inp_dict.get("org"),
            "ip_str": inp_dict.get("ip_str"),

        }

        cur_hash = inp_dict.get("hash")
        cur_data = {
            "data": inp_dict.get("data"),
            "port": inp_dict.get("port"),
            "os": inp_dict.get("os"),
            "http": inp_dict.get("http"),
            "timestamp": inp_dict.get("timestamp"),
        }

        # Doesn't exist
        if not returnables.get(cur_ip):
            uniq_dict["data"] = dict({cur_hash: cur_data})
            returnables[cur_ip] = uniq_dict
            continue

        returnables.get(cur_ip).get("data")[cur_hash] = cur_data

    return returnables.values()