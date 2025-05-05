from models import db
from datetime import datetime

class VolunteerAssignment(db.Model):
    __tablename__ = 'volunteer_assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.volunteer_id'))
    camp_id = db.Column(db.Integer, db.ForeignKey('relief_camps.camp_id'))
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    end_date = db.Column(db.Date)
    
    # Define relationships
    volunteer = db.relationship('Volunteer', backref='assignments')
    camp = db.relationship('ReliefCamp', backref='volunteer_assignments')
    
    def to_dict(self):
        return {
            'assignment_id': self.assignment_id,
            'volunteer_id': self.volunteer_id,
            'camp_id': self.camp_id,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None
        }
    
    def to_dict_with_details(self):
        result = self.to_dict()
        
        if self.volunteer:
            result['volunteer'] = {
                'volunteer_id': self.volunteer.volunteer_id,
                'first_name': self.volunteer.first_name,
                'last_name': self.volunteer.last_name,
                'contact_number': self.volunteer.contact_number,
                'skills': self.volunteer.skills
            }
            
        if self.camp:
            result['camp'] = {
                'camp_id': self.camp.camp_id,
                'camp_name': self.camp.camp_name,
                'location': self.camp.location
            }
                
        return result 