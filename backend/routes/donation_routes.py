from flask import Blueprint, request, jsonify
from models import db
from models.donation import Donation
from datetime import datetime

donation_bp = Blueprint('donation', __name__, url_prefix='/donations')

@donation_bp.route('', methods=['POST'])
def add_donation():
    data = request.get_json()
    
    try:
        date_donated = None
        if data.get('date_donated'):
            date_donated = datetime.strptime(data.get('date_donated'), '%Y-%m-%d').date()
        
        new_donation = Donation(
            donor_id=data.get('donor_id'),
            item_id=data.get('item_id'),
            quantity=data.get('quantity', 0),
            date_donated=date_donated
        )
        
        db.session.add(new_donation)
        db.session.commit()
        
        return jsonify({'message': 'Donation entry added successfully', 'donation': new_donation.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@donation_bp.route('', methods=['GET'])
def get_all_donations():
    donations = Donation.query.all()
    result = [donation.to_dict_with_details() for donation in donations]
    return jsonify(result)

@donation_bp.route('/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    return jsonify(donation.to_dict_with_details())

@donation_bp.route('/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    data = request.get_json()
    
    try:
        if 'donor_id' in data:
            donation.donor_id = data['donor_id']
        if 'item_id' in data:
            donation.item_id = data['item_id']
        if 'quantity' in data:
            donation.quantity = data['quantity']
        if 'date_donated' in data:
            donation.date_donated = datetime.strptime(data['date_donated'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Donation updated successfully', 'donation': donation.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@donation_bp.route('/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    
    try:
        db.session.delete(donation)
        db.session.commit()
        return jsonify({'message': 'Donation record deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 