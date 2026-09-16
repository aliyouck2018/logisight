"""Transport Route model."""

from app import db
from app.models.base import BaseModel


class TransportRoute(BaseModel):
    """Transport Route model for tracking transport routes."""
    
    route_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    shipment_id = db.Column(db.String(50), db.ForeignKey('shipment.shipment_id'), nullable=False, index=True)
    departure_location = db.Column(db.String(255), nullable=False)
    arrival_location = db.Column(db.String(255), nullable=False)
    transport_mode = db.Column(db.String(50), nullable=False)  # air, sea, truck, rail, multimodal
    distance = db.Column(db.Float, nullable=True)  # in km
    estimated_duration = db.Column(db.Integer, nullable=True)  # in hours
    actual_duration = db.Column(db.Integer, nullable=True)  # in hours
    cost = db.Column(db.Float, nullable=True)
    cost_currency = db.Column(db.String(3), default='USD', nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, in_transit, completed, delayed
    scheduled_departure = db.Column(db.DateTime, nullable=True)
    actual_departure = db.Column(db.DateTime, nullable=True)
    scheduled_arrival = db.Column(db.DateTime, nullable=True)
    actual_arrival = db.Column(db.DateTime, nullable=True)
    carrier_name = db.Column(db.String(255), nullable=True)
    vehicle_id = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'route_id': self.route_id,
            'shipment_id': self.shipment_id,
            'departure_location': self.departure_location,
            'arrival_location': self.arrival_location,
            'transport_mode': self.transport_mode,
            'distance': self.distance,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'cost': self.cost,
            'cost_currency': self.cost_currency,
            'status': self.status,
            'scheduled_departure': self.scheduled_departure.isoformat() if self.scheduled_departure else None,
            'actual_departure': self.actual_departure.isoformat() if self.actual_departure else None,
            'scheduled_arrival': self.scheduled_arrival.isoformat() if self.scheduled_arrival else None,
            'actual_arrival': self.actual_arrival.isoformat() if self.actual_arrival else None,
            'carrier_name': self.carrier_name,
            'vehicle_id': self.vehicle_id,
            'notes': self.notes,
        })
        return data
