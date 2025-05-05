from models import db
from datetime import datetime

class Supply(db.Model):
    __tablename__ = 'supplies'
    
    supply_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'))
    camp_id = db.Column(db.Integer, db.ForeignKey('relief_camps.camp_id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    date_received = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Define relationships
    camp = db.relationship('ReliefCamp', backref='supplies')
    inventory_item = db.relationship('Inventory', backref='supplies')
    
    def to_dict(self):
        return {
            'supply_id': self.supply_id,
            'item_id': self.item_id,
            'camp_id': self.camp_id,
            'quantity': self.quantity,
            'date_received': self.date_received.strftime('%Y-%m-%d') if self.date_received else None
        }
    
    def to_dict_with_details(self):
        result = self.to_dict()
        
        if self.camp:
            result['camp'] = {
                'camp_id': self.camp.camp_id,
                'camp_name': self.camp.camp_name,
                'location': self.camp.location
            }
            
        if self.inventory_item:
            result['item'] = {
                'item_id': self.inventory_item.item_id,
                'item_name': self.inventory_item.item_name
            }
                
        return result 