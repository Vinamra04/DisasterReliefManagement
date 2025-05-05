from flask import Blueprint, request, jsonify
from models import db
from models.donor import Donor
from datetime import datetime

donor_bp = Blueprint('donor', __name__, url_prefix='/donors')

@donor_bp.route('', methods=['POST'])
def add_donor():
    data = request.get_json()
    
    try:
        date_donated = None
        if data.get('date_donated'):
            date_donated = datetime.strptime(data.get('date_donated'), '%Y-%m-%d').date()
        
        new_donor = Donor(
            donor_name=data.get('donor_name'),
            item_id=data.get('item_id'),
            quantity=data.get('quantity', 0),
            date_donated=date_donated
        )
        
        db.session.add(new_donor)
        db.session.commit()
        
        return jsonify({'message': 'Donor entry added successfully', 'donor': new_donor.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@donor_bp.route('', methods=['GET'])
def get_all_donors():
    donors = Donor.query.all()
    result = [donor.to_dict_with_item() for donor in donors]
    return jsonify(result)

@donor_bp.route('/<int:donor_id>', methods=['GET'])
def get_donor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    return jsonify(donor.to_dict_with_item())

@donor_bp.route('/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    data = request.get_json()
    
    try:
        if 'donor_name' in data:
            donor.donor_name = data['donor_name']
        if 'item_id' in data:
            donor.item_id = data['item_id']
        if 'quantity' in data:
            donor.quantity = data['quantity']
        if 'date_donated' in data:
            donor.date_donated = datetime.strptime(data['date_donated'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Donor information updated successfully', 'donor': donor.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@donor_bp.route('/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    
    try:
        db.session.delete(donor)
        db.session.commit()
        return jsonify({'message': 'Donor record deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 