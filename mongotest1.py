from pymongo import MongoClient
import os

# Use environment variables for sensitive information
mongo_uri = os.getenv('mongodb+srv://dasun:dasun@iotpro1.yyjh3qr.mongodb.net/?retryWrites=true&w=majority&appName=iotpro1')
db_name = os.getenv('DB_NAME', 'test')
collection_name = os.getenv('COLLECTION_NAME', 'test')

# Establish a connection to the MongoDB cluster
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

supplier_data = {
    '_id': 7,  # Unique identifier
    'supplier_id': 323,
    'user_name': "sfghsfd",
    'mobile_number': 234,
    'address': "dfgsdfg",
    'type_of_goods': "dgdfgdfg"
}


result = collection.insert_one(supplier_data)
    
if result.inserted_id:
    print("Data successfully inserted for supplier.")

