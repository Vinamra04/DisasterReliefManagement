from flask import Blueprint, request, jsonify
from models import db
from models.volunteer_assignment import VolunteerAssignment
from datetime import datetime

assignment_bp = Blueprint('assignment', __name__, url_prefix='/assignments')

@assignment_bp.route('', methods=['POST'])
def add_assignment():
    data = request.get_json()
    
    try:
        # Parse dates from strings
        start_date = None
        if data.get('start_date'):
            start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        
        end_date = None
        if data.get('end_date'):
            end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        
        new_assignment = VolunteerAssignment(
            volunteer_id=data.get('volunteer_id'),
            camp_id=data.get('camp_id'),
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(new_assignment)
        db.session.commit()
        
        return jsonify({'message': 'Volunteer assigned successfully', 'assignment': new_assignment.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@assignment_bp.route('', methods=['GET'])
def get_all_assignments():
    assignments = VolunteerAssignment.query.all()
    result = [assignment.to_dict_with_details() for assignment in assignments]
    return jsonify(result)

@assignment_bp.route('/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    assignment = VolunteerAssignment.query.get_or_404(assignment_id)
    return jsonify(assignment.to_dict_with_details())

@assignment_bp.route('/<int:assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    assignment = VolunteerAssignment.query.get_or_404(assignment_id)
    data = request.get_json()
    
    try:
        if 'volunteer_id' in data:
            assignment.volunteer_id = data['volunteer_id']
        if 'camp_id' in data:
            assignment.camp_id = data['camp_id']
        if 'start_date' in data:
            assignment.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            assignment.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None
        
        db.session.commit()
        return jsonify({'message': 'Assignment updated successfully', 'assignment': assignment.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@assignment_bp.route('/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    assignment = VolunteerAssignment.query.get_or_404(assignment_id)
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({'message': 'Assignment deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 