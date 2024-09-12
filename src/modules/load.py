from modules.load_modules.mongoLoad import mongoLoad

class Load(): 
    def __init__(self, mongo_url, mongo_db) -> None:
        self.mongo = mongoLoad(mongo_url=mongo_url, mongo_db=mongo_db)

    def post(self, inp: list[dict]) -> bool: 
        success = True 

        for inp_dict in inp: 
            inp_ip = inp_dict.get("ip_str")

            cur_entry = self.mongo.get("1.1.1.1") 

            if not cur_entry: 
                success &= self.mongo.post(inp_dict)
                continue
            
            pass
            
