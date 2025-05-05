from models import db

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    
    volunteer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20))
    skills = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'volunteer_id': self.volunteer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'contact_number': self.contact_number,
            'skills': self.skills
        } 