from models import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey('relief_camps.camp_id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    date_received = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Define relationship
    camp = db.relationship('ReliefCamp', backref='inventory_items')
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'camp_id': self.camp_id,
            'quantity': self.quantity,
            'date_received': self.date_received.strftime('%Y-%m-%d') if self.date_received else None
        }
    
    def to_dict_with_camp(self):
        result = self.to_dict()
        if self.camp:
            result['camp'] = {
                'camp_id': self.camp.camp_id,
                'camp_name': self.camp.camp_name,
                'location': self.camp.location
            }
        return result 