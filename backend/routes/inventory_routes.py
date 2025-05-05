from flask import Blueprint, request, jsonify
from models import db
from models.inventory import Inventory
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('', methods=['POST'])
def add_inventory():
    data = request.get_json()
    
    try:
        date_received = None
        if data.get('date_received'):
            date_received = datetime.strptime(data.get('date_received'), '%Y-%m-%d').date()
        
        new_item = Inventory(
            item_name=data.get('item_name'),
            camp_id=data.get('camp_id'),
            quantity=data.get('quantity', 0),
            date_received=date_received
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({'message': 'Inventory item added successfully', 'item': new_item.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@inventory_bp.route('', methods=['GET'])
def get_all_inventory():
    items = Inventory.query.all()
    result = [item.to_dict_with_camp() for item in items]
    return jsonify(result)

@inventory_bp.route('/<int:item_id>', methods=['GET'])
def get_inventory(item_id):
    item = Inventory.query.get_or_404(item_id)
    return jsonify(item.to_dict_with_camp())

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_inventory(item_id):
    item = Inventory.query.get_or_404(item_id)
    data = request.get_json()
    
    try:
        if 'item_name' in data:
            item.item_name = data['item_name']
        if 'camp_id' in data:
            item.camp_id = data['camp_id']
        if 'quantity' in data:
            item.quantity = data['quantity']
        if 'date_received' in data:
            item.date_received = datetime.strptime(data['date_received'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Inventory item updated successfully', 'item': item.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_inventory(item_id):
    item = Inventory.query.get_or_404(item_id)
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Inventory item deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 