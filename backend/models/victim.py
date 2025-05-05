from models import db
from datetime import datetime

class VictimSurvivor(db.Model):
    __tablename__ = 'victim_survivors'
    
    victim_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_no = db.Column(db.String(20))
    address = db.Column(db.String(255))
    camp_id = db.Column(db.Integer, db.ForeignKey('relief_camps.camp_id'))
    
    # Relationship with ReliefCamp
    # camp = db.relationship('ReliefCamp', backref='victims')
    
    def to_dict(self):
        return {
            'victim_id': self.victim_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'contact_no': self.contact_no,
            'address': self.address,
            'camp_id': self.camp_id
        } 