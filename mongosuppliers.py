# mongodb_utils.py

from pymongo import MongoClient

def insert_supplier_data(supplier_id, user_name, mobile_number, address, type_of_goods):
    cluster = MongoClient('mongodb+srv://dasun:dasun@iotpro1.yyjh3qr.mongodb.net/?retryWrites=true&w=majority&appName=iotpro1')
    db = cluster["test"]
    collection = db["test"]

    supplier_data = {
        'supplier_id': supplier_id,
        'user_name': user_name,
        'mobile_number': mobile_number,
        'address': address,
        'type_of_goods': type_of_goods
    }

    collection.insert_one(supplier_data)
    print(f"Data inserted for supplier: {user_name}")
