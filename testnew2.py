from mongosupplies import insert_supplies_data
from mongosuppliers import insert_supplier_data
from placeitemdata import insert_place_itam
from editshell import edit_shell
from realrun2 import homearm


from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/place_item', methods=['POST'])
def place_item():
    data = request.json 

    item_number = data.get('itemNumber')
    supplies_id = data.get('suppliesId')
    shelf_number = data.get('shelfNumber')

    print(f"Received data: Item Number: {item_number}, Supplies ID: {supplies_id}, Shelf Number: {shelf_number}")
    print("new")
    insert_place_itam(supplies_id, shelf_number, item_number)

    homearm()

    return jsonify({'status': 'success', 'message': 'Item placed successfully'}), 200
    

@app.route('/retrieve_item_data', methods=['POST'])
def retrieve_item_data():
    data = request.json
    item_number = data.get('itemNumber')
    shelf_number = item_number
    print(f'Retrieve Item Page: {item_number}')
    edit_shell(shelf_number)

    return jsonify({'status': 'success', 'page': 'RetrieveItemPage', 'itemNumber': item_number}), 200

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    data = request.json
    supplier_id = data.get('supplierId')
    user_name = data.get('userName')
    mobile_number = data.get('mobileNumber')
    address = data.get('address')
    type_of_goods = data.get('typeOfGoods')
    print(f"Added Supplier: ID={supplier_id}, Name={user_name}, Mobile={mobile_number}, Address={address}, Goods={type_of_goods}")
    insert_supplier_data(supplier_id, user_name, mobile_number, address, type_of_goods)
    return jsonify({'status': 'success', 'page': 'AddSupplierPage', 'supplierId': supplier_id, 'userName': user_name, 'mobileNumber': mobile_number, 'address': address, 'typeOfGoods': type_of_goods}), 200

@app.route('/add_supplies', methods=['POST'])
def add_supplies():
    data = request.json
    supplier_id = data.get('supplierId')
    quantity_count = data.get('quantityCount')
    unit_cost = data.get('unitCost')
    total_cost = data.get('totalCost')
    type_of_goods = data.get('typeOfGoods')
    estimated_delivery_date = data.get('estimatedDeliveryDate')
    delivered_date = data.get('deliveredDate')
    delivery_status = data.get('deliveryStatus')
    supplies_id = data.get('suppliesId')

    if estimated_delivery_date:
        estimated_delivery_date = datetime.strptime(estimated_delivery_date, '%Y-%m-%d')
    if delivered_date:
        delivered_date = datetime.strptime(delivered_date, '%Y-%m-%d')

    print(f"Added Supplies: Suppplies id {supplies_id} Supplier ID={supplier_id}, Quantity={quantity_count}, Unit Cost={unit_cost}, Total Cost={total_cost}, Goods={type_of_goods}, Estimated Delivery={estimated_delivery_date}, Delivered={delivered_date}, Status={delivery_status}")
    insert_supplies_data(supplier_id, quantity_count, unit_cost, total_cost, type_of_goods, estimated_delivery_date, delivered_date, delivery_status, supplies_id)


    return jsonify({
        'status': 'success',
        'page': 'AddSuppliesPage',
        'supplierId': supplier_id,
        'quantityCount': quantity_count,
        'unitCost': unit_cost,
        'totalCost': total_cost,
        'typeOfGoods': type_of_goods,
        'estimatedDeliveryDate': str(estimated_delivery_date) if estimated_delivery_date else None,
        'deliveredDate': str(delivered_date) if delivered_date else None,
        'deliveryStatus': delivery_status
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
