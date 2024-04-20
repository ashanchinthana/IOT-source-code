from pymongo import MongoClient
from datetime import datetime
from incount import incountdb

def insert_place_itam(supplies_id, shelf_number, item_number):
    cluster = MongoClient('mongodb+srv://dasun:dasun@iotpro1.yyjh3qr.mongodb.net/?retryWrites=true&w=majority&appName=iotpro1')
    db = cluster["test"]
    collection = db["shell"]





    state=1
    order_data = {
        'item_number': item_number,
        'supplies_id': supplies_id,
        'state': state
    }

    result = collection.update_one({"shelf_number": shelf_number}, {"$set": order_data})

    if result.matched_count > 0:  # Check if the update matched any document
        print(f"Order data successfully updated for shelf number: {shelf_number}")
        incountdb(supplies_id, item_number)  # Perform the additional action if update is successful
    else:
        print("Failed to update order data. No matching document found.")
