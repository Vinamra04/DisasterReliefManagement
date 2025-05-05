from flask import Blueprint, request, jsonify
from models import db
from models.missing_person import MissingPersonReport
from datetime import datetime

missing_bp = Blueprint('missing', __name__, url_prefix='/missing-reports')

@missing_bp.route('', methods=['POST'])
def add_missing_report():
    data = request.get_json()
    
    try:
        new_report = MissingPersonReport(
            reporter_name=data.get('reporter_name'),
            missing_person_name=data.get('missing_person_name'),
            last_seen_location=data.get('last_seen_location'),
            date_reported=datetime.strptime(data.get('date_reported'), '%Y-%m-%d').date() if data.get('date_reported') else datetime.utcnow().date(),
            contact=data.get('contact'),
            camp_id=data.get('camp_id'),
            victim_id=data.get('victim_id')
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        return jsonify({'message': 'Missing person report submitted successfully', 'report': new_report.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@missing_bp.route('', methods=['GET'])
def get_all_reports():
    reports = MissingPersonReport.query.all()
    result = [report.to_dict_with_details() for report in reports]
    return jsonify(result)

@missing_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    report = MissingPersonReport.query.get_or_404(report_id)
    return jsonify(report.to_dict_with_details())

@missing_bp.route('/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    report = MissingPersonReport.query.get_or_404(report_id)
    data = request.get_json()
    
    try:
        if 'reporter_name' in data:
            report.reporter_name = data['reporter_name']
        if 'missing_person_name' in data:
            report.missing_person_name = data['missing_person_name']
        if 'last_seen_location' in data:
            report.last_seen_location = data['last_seen_location']
        if 'date_reported' in data:
            report.date_reported = datetime.strptime(data['date_reported'], '%Y-%m-%d').date()
        if 'contact' in data:
            report.contact = data['contact']
        if 'camp_id' in data:
            report.camp_id = data['camp_id']
        if 'victim_id' in data:
            report.victim_id = data['victim_id']
        
        db.session.commit()
        return jsonify({'message': 'Missing person report updated successfully', 'report': report.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@missing_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    report = MissingPersonReport.query.get_or_404(report_id)
    
    try:
        db.session.delete(report)
        db.session.commit()
        return jsonify({'message': 'Missing person report deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400