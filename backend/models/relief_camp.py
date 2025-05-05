from models import db

class ReliefCamp(db.Model):
    __tablename__ = 'relief_camps'
    
    camp_id = db.Column(db.Integer, primary_key=True)
    camp_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    contact_person = db.Column(db.String(100))
    
    # Define relationships
    victims = db.relationship('VictimSurvivor', backref='camp', lazy=True)
    missing_reports = db.relationship('MissingPersonReport', backref='camp', lazy=True)
    
    def to_dict(self):
        return {
            'camp_id': self.camp_id,
            'camp_name': self.camp_name,
            'location': self.location,
            'capacity': self.capacity,
            'contact_person': self.contact_person
        } 