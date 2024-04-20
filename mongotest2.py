import pymongo
from pymongo import MongoClient
import os

# Use environment variables for sensitive information

cluster = MongoClient('mongodb+srv://dasun:dasun@iotpro1.yyjh3qr.mongodb.net/?retryWrites=true&w=majority&appName=iotpro1')

db = cluster["test"]
collection = db["test"]

supplier_data = {
    '_id': 8,  # Unique identifier
    'supplier_id': 323,
    'user_name': "sfghsfd",
    'mobile_number': 234,
    'address': "dfgsdfg",
    'type_of_goods': "dgdfgdfg"
}

result = collection.insert_one(supplier_data)
    
if result.inserted_id:
    print("Data successfully inserted for supplier.")
