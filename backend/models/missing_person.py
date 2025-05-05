from models import db
from datetime import datetime

class MissingPersonReport(db.Model):
    __tablename__ = 'missing_person_reports'
    
    report_id = db.Column(db.Integer, primary_key=True)
    reporter_name = db.Column(db.String(100), nullable=False)
    missing_person_name = db.Column(db.String(100), nullable=False)
    last_seen_location = db.Column(db.String(255))
    date_reported = db.Column(db.Date, default=datetime.utcnow().date)
    contact = db.Column(db.String(100))
    camp_id = db.Column(db.Integer, db.ForeignKey('relief_camps.camp_id'))
    victim_id = db.Column(db.Integer, db.ForeignKey('victim_survivors.victim_id'))
    
    # Define relationships
    camp = db.relationship('ReliefCamp', backref='missing_reports')
    victim = db.relationship('VictimSurvivor', backref='missing_reports')
    
    def to_dict(self):
        return {
            'report_id': self.report_id,
            'reporter_name': self.reporter_name,
            'missing_person_name': self.missing_person_name,
            'last_seen_location': self.last_seen_location,
            'date_reported': self.date_reported.strftime('%Y-%m-%d') if self.date_reported else None,
            'contact': self.contact,
            'camp_id': self.camp_id,
            'victim_id': self.victim_id
        }
    
    def to_dict_with_details(self):
        result = self.to_dict()
        
        if self.victim:
            result['victim'] = {
                'victim_id': self.victim.victim_id,
                'first_name': self.victim.first_name,
                'last_name': self.victim.last_name,
                'contact_no': self.victim.contact_no
            }
            
        if self.camp:
            result['camp'] = {
                'camp_id': self.camp.camp_id,
                'camp_name': self.camp.camp_name,
                'location': self.camp.location
            }
                
        return result 