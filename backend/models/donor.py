from models import db
from datetime import datetime

class Donor(db.Model):
    __tablename__ = 'donors'
    
    donor_id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    date_donated = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Define relationship
    inventory_item = db.relationship('Inventory', backref='donors')
    
    def to_dict(self):
        return {
            'donor_id': self.donor_id,
            'donor_name': self.donor_name,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'date_donated': self.date_donated.strftime('%Y-%m-%d') if self.date_donated else None
        }
    
    def to_dict_with_item(self):
        result = self.to_dict()
        if self.inventory_item:
            result['item'] = {
                'item_id': self.inventory_item.item_id,
                'item_name': self.inventory_item.item_name,
                'camp_id': self.inventory_item.camp_id
            }
        return result 