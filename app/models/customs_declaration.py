"""Customs Declaration model."""

from app import db
from app.models.base import BaseModel


class CustomsDeclaration(BaseModel):
    """Customs Declaration model for tracking customs data."""
    
    declaration_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    shipment_id = db.Column(db.String(50), db.ForeignKey('shipment.shipment_id'), nullable=False, index=True)
    hs_code = db.Column(db.String(20), nullable=False)  # Harmonized System code
    description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kg, pcs, etc.
    declared_value = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD', nullable=False)
    country_of_origin = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, approved, rejected, hold
    declaration_date = db.Column(db.DateTime, nullable=False)
    approval_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'declaration_id': self.declaration_id,
            'shipment_id': self.shipment_id,
            'hs_code': self.hs_code,
            'description': self.description,
            'quantity': self.quantity,
            'unit': self.unit,
            'declared_value': self.declared_value,
            'currency': self.currency,
            'country_of_origin': self.country_of_origin,
            'status': self.status,
            'declaration_date': self.declaration_date.isoformat() if self.declaration_date else None,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'notes': self.notes,
        })
        return data
