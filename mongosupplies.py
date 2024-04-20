from insertquantity import insert_quantity

# mongodb_utils.py

from pymongo import MongoClient
from datetime import datetime

def insert_supplies_data(supplier_id, quantity_count, unit_cost, total_cost, type_of_goods, estimated_delivery_date, delivered_date, delivery_status, supplies_id):
    cluster = MongoClient('mongodb+srv://dasun:dasun@iotpro1.yyjh3qr.mongodb.net/?retryWrites=true&w=majority&appName=iotpro1')
    db = cluster["test"]
    collection = db["supplies"]


    # Ensure that dates are in the appropriate datetime format
    if isinstance(estimated_delivery_date, str):
        estimated_delivery_date = datetime.strptime(estimated_delivery_date, '%Y-%m-%d')
    if isinstance(delivered_date, str):
        delivered_date = datetime.strptime(delivered_date, '%Y-%m-%d')

    order_data = {

        'supplies_id': supplies_id,
        'supplier_id': supplier_id,
        'quantity_count': quantity_count,
        'unit_cost': unit_cost,
        'total_cost': total_cost,
        'type_of_goods': type_of_goods,
        'estimated_delivery_date': estimated_delivery_date,
        'delivered_date': delivered_date,
        'delivery_status': delivery_status

    }

    result = collection.insert_one(order_data)

    if result.inserted_id:
        print(f"Order data successfully inserted. Document ID: {result.inserted_id}")
        insert_quantity(supplies_id, quantity_count, type_of_goods)
    else:
        print("Failed to insert order data.")
