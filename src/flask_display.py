from flask import Flask, jsonify
from pymongo import MongoClient
from lib.env_util import get_env_variable

app = Flask(__name__)
    
mongo_user = get_env_variable("MONGO_INITDB_ROOT_USERNAME")
mongo_password = get_env_variable("MONGO_INITDB_ROOT_PASSWORD")
mongo_db = get_env_variable("MONGO_DB")

# MongoDB connection setup
mongo_client = MongoClient(
    "mongodb",
    username=mongo_user,
    password=mongo_password,
)
db = mongo_client[mongo_db]
collection = db["ip-information"]

@app.route('/')
def index():
    return "Welcome to the IP Information Dashboard!"

@app.route('/statistics')
def statistics():
    # Count the total number of records
    total_records = collection.count_documents({})

    # Get unique cities
    unique_cities = collection.distinct("city")

    # Get most common content
    most_common_content = collection.aggregate([
        {"$group": {"_id": "$data", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])

    # Format the result
    most_common_content = list(most_common_content)
    most_common_content = most_common_content[0]['_id'] if most_common_content else None

    # Prepare statistics
    statistics = {
        "total_records": total_records,
        "unique_cities": unique_cities,
        "most_common_content": most_common_content
    }

    return jsonify(statistics)

if __name__ == '__main__':
    app.run(debug=True)
