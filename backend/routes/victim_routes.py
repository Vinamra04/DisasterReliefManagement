from flask import Blueprint, request, jsonify
from models import db
from models.victim import VictimSurvivor
from datetime import datetime

victim_bp = Blueprint('victim', __name__, url_prefix='/victims')

@victim_bp.route('', methods=['POST'])
def add_victim():
    data = request.get_json()
    
    try:
        # Convert date string to date object
        date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None
        
        new_victim = VictimSurvivor(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=date_of_birth,
            contact_no=data.get('contact_no'),
            address=data.get('address'),
            camp_id=data.get('camp_id')
        )
        
        db.session.add(new_victim)
        db.session.commit()
        
        return jsonify({'message': 'Victim added successfully', 'victim': new_victim.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@victim_bp.route('/<int:victim_id>', methods=['PUT'])
def update_victim(victim_id):
    victim = VictimSurvivor.query.get_or_404(victim_id)
    data = request.get_json()
    
    try:
        if 'first_name' in data:
            victim.first_name = data['first_name']
        if 'last_name' in data:
            victim.last_name = data['last_name']
        if 'date_of_birth' in data:
            victim.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        if 'contact_no' in data:
            victim.contact_no = data['contact_no']
        if 'address' in data:
            victim.address = data['address']
        if 'camp_id' in data:
            victim.camp_id = data['camp_id']
        
        db.session.commit()
        return jsonify({'message': 'Victim updated successfully', 'victim': victim.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@victim_bp.route('', methods=['GET'])
def get_all_victims():
    victims = VictimSurvivor.query.all()
    result = [victim.to_dict() for victim in victims]
    return jsonify(result) 