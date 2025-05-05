from models import db
from datetime import datetime

class Donation(db.Model):
    __tablename__ = 'donations'
    
    donation_id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.donor_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    date_donated = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Define relationships
    donor = db.relationship('Donor', backref='donations')
    inventory_item = db.relationship('Inventory', backref='donations')
    
    def to_dict(self):
        return {
            'donation_id': self.donation_id,
            'donor_id': self.donor_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'date_donated': self.date_donated.strftime('%Y-%m-%d') if self.date_donated else None
        }
    
    def to_dict_with_details(self):
        result = self.to_dict()
        
        if self.donor:
            result['donor'] = {
                'donor_id': self.donor.donor_id,
                'donor_name': self.donor.donor_name
            }
            
        if self.inventory_item:
            result['item'] = {
                'item_id': self.inventory_item.item_id,
                'item_name': self.inventory_item.item_name,
                'camp_id': self.inventory_item.camp_id
            }
            
            # If the inventory item has a camp, include basic camp info
            if hasattr(self.inventory_item, 'camp') and self.inventory_item.camp:
                result['item']['camp'] = {
                    'camp_id': self.inventory_item.camp.camp_id,
                    'camp_name': self.inventory_item.camp.camp_name
                }
                
        return result 