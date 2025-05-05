from flask import Blueprint, request, jsonify
from models import db
from models.supply import Supply
from datetime import datetime

supply_bp = Blueprint('supply', __name__, url_prefix='/supplies')

@supply_bp.route('', methods=['POST'])
def add_supply():
    data = request.get_json()
    
    try:
        date_received = None
        if data.get('date_received'):
            date_received = datetime.strptime(data.get('date_received'), '%Y-%m-%d').date()
        
        new_supply = Supply(
            item_id=data.get('item_id'),
            camp_id=data.get('camp_id'),
            quantity=data.get('quantity', 0),
            date_received=date_received
        )
        
        db.session.add(new_supply)
        db.session.commit()
        
        return jsonify({'message': 'Supply record added successfully', 'supply': new_supply.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@supply_bp.route('', methods=['GET'])
def get_all_supplies():
    supplies = Supply.query.all()
    result = [supply.to_dict_with_details() for supply in supplies]
    return jsonify(result)

@supply_bp.route('/<int:supply_id>', methods=['GET'])
def get_supply(supply_id):
    supply = Supply.query.get_or_404(supply_id)
    return jsonify(supply.to_dict_with_details())

@supply_bp.route('/<int:supply_id>', methods=['PUT'])
def update_supply(supply_id):
    supply = Supply.query.get_or_404(supply_id)
    data = request.get_json()
    
    try:
        if 'item_id' in data:
            supply.item_id = data['item_id']
        if 'camp_id' in data:
            supply.camp_id = data['camp_id']
        if 'quantity' in data:
            supply.quantity = data['quantity']
        if 'date_received' in data:
            supply.date_received = datetime.strptime(data['date_received'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Supply information updated successfully', 'supply': supply.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@supply_bp.route('/<int:supply_id>', methods=['DELETE'])
def delete_supply(supply_id):
    supply = Supply.query.get_or_404(supply_id)
    
    try:
        db.session.delete(supply)
        db.session.commit()
        return jsonify({'message': 'Supply record deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 