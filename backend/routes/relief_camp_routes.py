from flask import Blueprint, request, jsonify
from models import db
from models.relief_camp import ReliefCamp

camp_bp = Blueprint('camp', __name__, url_prefix='/camps')

@camp_bp.route('', methods=['POST'])
def add_camp():
    data = request.get_json()
    
    try:
        new_camp = ReliefCamp(
            camp_name=data.get('camp_name'),
            location=data.get('location'),
            capacity=data.get('capacity'),
            contact_person=data.get('contact_person')
        )
        
        db.session.add(new_camp)
        db.session.commit()
        
        return jsonify({'message': 'Relief camp added successfully', 'camp': new_camp.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@camp_bp.route('', methods=['GET'])
def get_all_camps():
    camps = ReliefCamp.query.all()
    result = [camp.to_dict() for camp in camps]
    return jsonify(result)

@camp_bp.route('/<int:camp_id>', methods=['GET'])
def get_camp(camp_id):
    camp = ReliefCamp.query.get_or_404(camp_id)
    return jsonify(camp.to_dict())

@camp_bp.route('/<int:camp_id>', methods=['PUT'])
def update_camp(camp_id):
    camp = ReliefCamp.query.get_or_404(camp_id)
    data = request.get_json()
    
    try:
        if 'camp_name' in data:
            camp.camp_name = data['camp_name']
        if 'location' in data:
            camp.location = data['location']
        if 'capacity' in data:
            camp.capacity = data['capacity']
        if 'contact_person' in data:
            camp.contact_person = data['contact_person']
        
        db.session.commit()
        return jsonify({'message': 'Relief camp updated successfully', 'camp': camp.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@camp_bp.route('/<int:camp_id>', methods=['DELETE'])
def delete_camp(camp_id):
    camp = ReliefCamp.query.get_or_404(camp_id)
    
    try:
        db.session.delete(camp)
        db.session.commit()
        return jsonify({'message': 'Relief camp deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 