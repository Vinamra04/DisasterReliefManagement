from flask import Blueprint, request, jsonify
from models import db
from models.volunteer import Volunteer

volunteer_bp = Blueprint('volunteer', __name__, url_prefix='/volunteers')

@volunteer_bp.route('', methods=['POST'])
def add_volunteer():
    data = request.get_json()
    
    try:
        new_volunteer = Volunteer(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            contact_number=data.get('contact_number'),
            skills=data.get('skills')
        )
        
        db.session.add(new_volunteer)
        db.session.commit()
        
        return jsonify({'message': 'Volunteer added successfully', 'volunteer': new_volunteer.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@volunteer_bp.route('', methods=['GET'])
def get_all_volunteers():
    volunteers = Volunteer.query.all()
    result = [volunteer.to_dict() for volunteer in volunteers]
    return jsonify(result)

@volunteer_bp.route('/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    return jsonify(volunteer.to_dict())

@volunteer_bp.route('/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    data = request.get_json()
    
    try:
        if 'first_name' in data:
            volunteer.first_name = data['first_name']
        if 'last_name' in data:
            volunteer.last_name = data['last_name']
        if 'contact_number' in data:
            volunteer.contact_number = data['contact_number']
        if 'skills' in data:
            volunteer.skills = data['skills']
        
        db.session.commit()
        return jsonify({'message': 'Volunteer information updated successfully', 'volunteer': volunteer.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@volunteer_bp.route('/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    
    try:
        db.session.delete(volunteer)
        db.session.commit()
        return jsonify({'message': 'Volunteer deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400