from modules.load_modules.mongoLoad import mongoLoad

class Load(): 
    def __init__(self, mongo_url, mongo_db) -> None:
        self.mongo = mongoLoad(mongo_url=mongo_url, mongo_db=mongo_db)

    def post(self, inp: list[dict]) -> bool: 
        success = True 

        for inp_dict in inp: 
            success &= self.mongo.post(inp_dict)
            
        return success 
            
