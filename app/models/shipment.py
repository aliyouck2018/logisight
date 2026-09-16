"""Shipment model."""

from app import db
from app.models.base import BaseModel


class Shipment(BaseModel):
    """Shipment model for tracking shipments."""
    
    shipment_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    origin = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, in_transit, delivered, cancelled
    weight = db.Column(db.Float, nullable=True)  # in kg
    value = db.Column(db.Float, nullable=True)  # in currency
    carrier = db.Column(db.String(100), nullable=True)
    tracking_number = db.Column(db.String(100), nullable=True, index=True)
    departure_date = db.Column(db.DateTime, nullable=True)
    arrival_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'shipment_id': self.shipment_id,
            'origin': self.origin,
            'destination': self.destination,
            'status': self.status,
            'weight': self.weight,
            'value': self.value,
            'carrier': self.carrier,
            'tracking_number': self.tracking_number,
            'departure_date': self.departure_date.isoformat() if self.departure_date else None,
            'arrival_date': self.arrival_date.isoformat() if self.arrival_date else None,
            'notes': self.notes,
        })
        return data
