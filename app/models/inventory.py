"""Inventory model."""

from app import db
from app.models.base import BaseModel


class Inventory(BaseModel):
    """Inventory model for tracking inventory items."""
    
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Float, default=0, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kg, pcs, liters, etc.
    reorder_level = db.Column(db.Float, nullable=True)
    reorder_quantity = db.Column(db.Float, nullable=True)
    unit_cost = db.Column(db.Float, nullable=True)
    cost_currency = db.Column(db.String(3), default='USD', nullable=False)
    supplier = db.Column(db.String(255), nullable=True)
    last_restocked = db.Column(db.DateTime, nullable=True)
    expiration_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'sku': self.sku,
            'product_name': self.product_name,
            'description': self.description,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'reorder_level': self.reorder_level,
            'reorder_quantity': self.reorder_quantity,
            'unit_cost': self.unit_cost,
            'cost_currency': self.cost_currency,
            'supplier': self.supplier,
            'last_restocked': self.last_restocked.isoformat() if self.last_restocked else None,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'notes': self.notes,
        })
        return data
